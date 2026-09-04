const $ = (selector, root = document) => root.querySelector(selector);
const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];

const primaryNav = $('.topbar nav');
if (primaryNav && !primaryNav.querySelector('[data-profile-link]')) {
  const profileLink = document.createElement('a');
  profileLink.href = './profile.html';
  profileLink.textContent = 'Profile';
  profileLink.dataset.profileLink = 'true';
  primaryNav.prepend(profileLink);
}

const themeToggle = $('#theme-toggle');
const savedTheme = localStorage.getItem('derama-theme');
if (savedTheme === 'light') document.documentElement.dataset.theme = 'light';
themeToggle?.setAttribute('aria-pressed', String(document.documentElement.dataset.theme === 'light'));
themeToggle?.addEventListener('click', () => {
  const next = document.documentElement.dataset.theme === 'light' ? 'dark' : 'light';
  document.documentElement.dataset.theme = next;
  localStorage.setItem('derama-theme', next);
  themeToggle.setAttribute('aria-pressed', String(next === 'light'));
});

const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      revealObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.12 });
$$('.reveal').forEach((node) => revealObserver.observe(node));

const filters = $$('.filter');
const cards = $$('.evidence-card');
filters.forEach((button) => button.addEventListener('click', () => {
  const filter = button.dataset.filter;
  filters.forEach((item) => {
    const active = item === button;
    item.classList.toggle('active', active);
    item.setAttribute('aria-pressed', String(active));
  });
  cards.forEach((card) => {
    card.hidden = filter !== 'all' && card.dataset.product !== filter;
  });
}));

const dialog = $('#image-dialog');
const dialogImage = $('#dialog-image');
const dialogTitle = $('#dialog-title');
$$('.capture').forEach((button) => button.addEventListener('click', () => {
  dialogImage.src = button.dataset.image;
  dialogImage.alt = button.dataset.title;
  dialogTitle.textContent = button.dataset.title;
  dialog.showModal();
}));
$('#dialog-close')?.addEventListener('click', () => dialog.close());
dialog?.addEventListener('click', (event) => {
  if (event.target === dialog) dialog.close();
});

$$('.capture img').forEach((image) => image.addEventListener('error', () => {
  image.closest('.capture')?.classList.add('image-error');
  image.alt = `${image.alt} — source image unavailable`;
}));

const encoder = new TextEncoder();
const digest = async (value) => {
  const buffer = await crypto.subtle.digest('SHA-256', encoder.encode(value));
  return [...new Uint8Array(buffer)].map((byte) => byte.toString(16).padStart(2, '0')).join('');
};

const initialRecords = [
  { id: 'EV-01', product: 'MAYA', claim: 'Mission workspace capture', source: 'maya-codex-nexus/main' },
  { id: 'EV-02', product: 'MAYA', claim: 'Scoped decision boundary', source: 'maya-codex-nexus/main' },
  { id: 'EV-03', product: 'AEGIS', claim: 'Guarded mission runtime', source: 'aegis-unified/main' },
  { id: 'EV-04', product: 'AEGIS', claim: 'Responsive event projection', source: 'aegis-unified/main' },
  { id: 'EV-05', product: 'CV', claim: 'Deterministic two-page professional dossier', source: 'maya-codex-nexus/CV.md' },
  { id: 'EV-06', product: 'PROFILE', claim: 'Public maturity disclosure', source: 'gonzo-max2/main' },
  { id: 'EV-07', product: 'LEDGER', claim: 'Browser-local SHA-256 validation', source: 'docs/app.js' },
];
let records = structuredClone(initialRecords);
let chain = [];

async function buildChain() {
  chain = [];
  let previous = 'GENESIS';
  for (let index = 0; index < records.length; index += 1) {
    const payload = JSON.stringify({ sequence: index + 1, ...records[index], previous });
    const hash = await digest(payload);
    chain.push({ ...records[index], sequence: index + 1, previous, hash, expectedPayload: payload });
    previous = hash;
  }
  renderChain(true);
}

async function validateChain() {
  let previous = 'GENESIS';
  const validity = [];
  for (let index = 0; index < chain.length; index += 1) {
    const record = chain[index];
    const payload = JSON.stringify({ sequence: index + 1, ...records[index], previous });
    const calculated = await digest(payload);
    const valid = calculated === record.hash && record.previous === previous;
    validity.push(valid);
    previous = record.hash;
  }
  return validity;
}

async function renderChain(forceValid = false) {
  const validity = forceValid ? chain.map(() => true) : await validateChain();
  const container = $('#chain');
  container.innerHTML = chain.map((record, index) => `
    <article class="receipt ${validity[index] ? '' : 'invalid'}">
      <span class="receipt-index">${String(record.sequence).padStart(2, '0')} / ${record.id}</span>
      <h3>${records[index].product}</h3>
      <p>${records[index].claim}</p>
      <code title="${record.hash}">${record.hash}</code>
      <small>${validity[index] ? 'RECEIPT VALID' : 'DEPENDENCY INVALID'}</small>
    </article>`).join('');
  const allValid = validity.every(Boolean);
  const state = $('#chain-state');
  state.classList.toggle('invalid', !allValid);
  state.classList.toggle('valid', allValid);
  state.innerHTML = `<i></i> ${allValid ? 'CHAIN VALID' : 'CHAIN FRACTURED'}`;
  $('#chain-root').textContent = `ROOT / ${chain.at(-1)?.hash.slice(0, 20).toUpperCase() ?? 'EMPTY'}`;
}

$('#tamper-chain')?.addEventListener('click', async () => {
  records[1].claim = records[1].claim.includes('MUTATED') ? 'Scoped decision boundary' : 'MUTATED / uncommitted claim';
  await renderChain(false);
});
$('#repair-chain')?.addEventListener('click', async () => {
  records = structuredClone(initialRecords);
  await buildChain();
});

function updateClock() {
  const formatter = new Intl.DateTimeFormat('en-GB', { timeZone: 'Europe/Sofia', hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false });
  $('#sofia-time').textContent = formatter.format(new Date());
}
updateClock();
setInterval(updateClock, 1000);
buildChain();
