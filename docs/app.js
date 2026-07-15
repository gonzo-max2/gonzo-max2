const state = {
  profile: null,
  activeSystem: 0,
  activePhase: 0,
  activeTrip: 0,
  activeProof: 0,
  motion: !matchMedia('(prefers-reduced-motion: reduce)').matches,
  ledger: [],
  merkle: [],
  animationFrames: new Set(),
};

const $ = (selector, root = document) => root.querySelector(selector);
const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];

const PHASES = [
  {
    id: 'observe',
    title: 'Observe',
    subtitle: 'Acquire truth',
    copy: 'Acquire workspace, runtime, policy, operator intent, and the current evidence boundary before planning any action.',
    evidence: [['Workspace', 'SCOPED'], ['Runtime', 'AUTHENTICATED'], ['Policy', 'LOADED']],
    point: [72, 328],
    offset: 940,
  },
  {
    id: 'frame',
    title: 'Frame',
    subtitle: 'Model the mission',
    copy: 'Convert the mission into a safe, display-ready model with explicit constraints, unknowns, and evidence requirements.',
    evidence: [['Intent', 'NORMALIZED'], ['Unknowns', 'EXPLICIT'], ['Evidence plan', 'BOUND']],
    point: [164, 186],
    offset: 770,
  },
  {
    id: 'decide',
    title: 'Decide',
    subtitle: 'Commit to a path',
    copy: 'Select an execution strategy, approval boundary, workspace mode, and verification ladder without hiding trade-offs.',
    evidence: [['Plan', 'COMMITTED'], ['Approval', 'RESOLVED'], ['Worktree', 'ISOLATED']],
    point: [256, 126],
    offset: 595,
  },
  {
    id: 'act',
    title: 'Act',
    subtitle: 'Execute safely',
    copy: 'Run tools, commands, edits, and specialists through constrained capabilities while preserving causal ordering.',
    evidence: [['Tools', 'SCOPED'], ['Events', 'ORDERED'], ['Artifacts', 'TRACKED']],
    point: [356, 196],
    offset: 410,
  },
  {
    id: 'verify',
    title: 'Verify',
    subtitle: 'Challenge the claim',
    copy: 'Inspect diffs, commands, test output, runtime behavior, contradictions, and failure recovery before claiming success.',
    evidence: [['Tests', 'PASSED'], ['Diff', 'INSPECTED'], ['Contradictions', 'NONE']],
    point: [454, 124],
    offset: 205,
  },
  {
    id: 'receipt',
    title: 'Receipt',
    subtitle: 'Persist proof',
    copy: 'Bind the outcome to exact artifacts, verification evidence, runtime state, and a stable completion receipt.',
    evidence: [['Outcome', 'VERIFIED'], ['Receipt', 'PERSISTED'], ['Origin', 'RESTORABLE']],
    point: [536, 84],
    offset: 0,
  },
];

const TRIP_STATES = [
  { title: 'Request', kicker: 'ROUTE CAPTURED', phoneTitle: 'Your route is ready', copy: 'Resolving pickup, destination, and rider constraints.', progress: 12, point: [80, 424], offset: 1080 },
  { title: 'Match', kicker: 'DRIVER MATCH', phoneTitle: 'Driver selected', copy: 'The closest qualified driver accepted your trip.', progress: 34, point: [250, 382], offset: 820 },
  { title: 'Arrival', kicker: 'ARRIVING NOW', phoneTitle: 'Your driver is near', copy: 'Live location and arrival context remain synchronized.', progress: 55, point: [420, 304], offset: 570 },
  { title: 'Trip', kicker: 'TRIP IN PROGRESS', phoneTitle: 'Moving safely', copy: 'Route, ETA, rider, driver, and safety state advance together.', progress: 78, point: [610, 224], offset: 290 },
  { title: 'Complete', kicker: 'TRIP COMPLETE', phoneTitle: 'Arrived', copy: 'Payment, receipt, rating, and trip evidence settle atomically.', progress: 100, point: [842, 116], offset: 0 },
];

const SYSTEM_PROOFS = {
  maya: [['Authority', 'EVENT-SOURCED'], ['Execution', 'TRANSACTIONAL'], ['Completion', 'RECEIPT-BACKED'], ['Failure', 'RECOVERABLE']],
  vozime: [['State', 'ROLE-AWARE'], ['Journey', 'DETERMINISTIC'], ['Feedback', 'REALTIME'], ['Trust', 'VISIBLE']],
  aurelis: [['Motion', 'VELOCITY-DRIVEN'], ['Audio', 'SYNCHRONIZED'], ['Effects', 'POOLED'], ['Frame', 'MEASURED']],
  derama: [['Audio', 'REALTIME-SAFE'], ['Workflow', 'COMPLETE'], ['Routing', 'AUTHORITATIVE'], ['Control', 'INSTRUMENT-GRADE']],
  'aether-rf': [['Input', 'REAL-ONLY'], ['Signal', 'CALIBRATED'], ['Confidence', 'VISIBLE'], ['Runtime', 'RESILIENT']],
  credtrace: [['Scan', 'BOUNDED'], ['Evidence', 'PERSISTENT'], ['Secrets', 'REDACTED'], ['Resume', 'SUPPORTED']],
  'ui-debug': [['Exceptions', 'FAIL-CLOSED'], ['A11y', 'AUDITED'], ['Network', 'INSPECTED'], ['Receipt', 'MACHINE-READABLE']],
  'aether-audio': [['DSP', 'NATIVE'], ['Modulation', 'REALTIME'], ['Visuals', 'STATE-BOUND'], ['Control', 'TACTILE']],
  blockchain: [['Hashes', 'SHA-256'], ['Receipts', 'CHAINED'], ['Merkle', 'AGGREGATED'], ['Status', 'RESEARCH']],
};

const SYSTEM_VISUALS = {
  maya: () => `
    <span class="visual-caption">CAUSAL RUNTIME / LIVE</span>
    <div class="visual-maya">
      <div class="vm-ring"></div><div class="vm-ring"></div><div class="vm-core">M</div>
      <i class="vm-node"></i><i class="vm-node"></i><i class="vm-node"></i>
    </div>`,
  vozime: () => `
    <span class="visual-caption">TRIP STATE / SYNCHRONIZED</span>
    <div class="visual-route"><svg viewBox="0 0 640 520" aria-hidden="true">
      <path class="route-bg" d="M72 412C150 368 212 430 294 330S430 292 502 204 550 88 594 104"/>
      <path class="route-fg" d="M72 412C150 368 212 430 294 330S430 292 502 204 550 88 594 104"/>
      <circle cx="72" cy="412" r="9"/><circle cx="294" cy="330" r="9"/><circle cx="502" cy="204" r="9"/><circle cx="594" cy="104" r="9"/>
    </svg></div>`,
  aurelis: () => `
    <span class="visual-caption">MOTION FIELD / 16.6 MS</span>
    <div class="visual-wave"><svg viewBox="0 0 680 420" aria-hidden="true"><path d="M20 286C96 286 104 76 192 98S300 328 396 204 496 46 660 86"/></svg></div>`,
  derama: () => `
    <span class="visual-caption">DSP GRAPH / 48 KHZ</span>
    <div class="visual-wave"><svg viewBox="0 0 680 420" aria-hidden="true"><path d="M20 210C44 210 50 136 76 136S110 292 140 292 172 76 204 76 244 334 278 334 318 112 348 112 388 266 420 266 462 154 490 154 530 240 560 240 608 190 660 190"/></svg></div>`,
  'aether-rf': () => `
    <span class="visual-caption">RF FIELD / CALIBRATED</span>
    <div class="visual-radar"><i class="radar-sweep"></i><i class="radar-target t1"></i><i class="radar-target t2"></i><i class="radar-target t3"></i></div>`,
  credtrace: () => `
    <span class="visual-caption">FORENSIC GRAPH / BOUNDED</span>
    <div class="visual-chain"><span>VOLUME</span><span>PROFILE</span><span>ARCHIVE</span><span>FINDING</span><span>EVIDENCE</span><span>RECEIPT</span></div>`,
  'ui-debug': () => `
    <span class="visual-caption">QUALITY FABRIC / FAIL-CLOSED</span>
    <div class="visual-chain"><span>RUNTIME</span><span>NETWORK</span><span>A11Y</span><span>CONSOLE</span><span>VISUAL</span><span>GATE</span></div>`,
  'aether-audio': () => `
    <span class="visual-caption">SPATIAL AUDIO / NATIVE DSP</span>
    <div class="visual-orbit"><div class="vo-ring"></div><div class="vo-ring"></div><div class="vo-core">A</div><i class="vo-node"></i><i class="vo-node"></i><i class="vo-node"></i></div>`,
  blockchain: () => `
    <span class="visual-caption">MERKLE FABRIC / RESEARCH</span>
    <div class="visual-chain"><span>INTENT</span><span>POLICY</span><span>ACTION</span><span>PROOF</span><span>ROOT</span><span>RECEIPT</span></div>`,
};

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, character => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
  })[character]);
}

async function loadProfile() {
  if (window.__PROFILE__) {
    state.profile = window.__PROFILE__;
  } else {
    const response = await fetch('./data/profile.json', { cache: 'no-store' });
    if (!response.ok) throw new Error(`Profile data HTTP ${response.status}`);
    state.profile = await response.json();
  }
  $('#hero-system-count').textContent = String(state.profile.systems.length).padStart(2, '0');
  $('#current-mission').textContent = state.profile.current.mission;
  renderAtlas();
  renderProofCases();
  renderMaturity();
}

function renderAtlas() {
  const rail = $('#atlas-rail');
  rail.textContent = '';
  state.profile.systems.forEach((system, index) => {
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'atlas-tab';
    button.role = 'tab';
    button.ariaSelected = String(index === state.activeSystem);
    button.style.setProperty('--tab-accent', system.accent);
    button.innerHTML = `
      <span class="tab-index">${String(index + 1).padStart(2, '0')}</span>
      <span class="tab-copy"><strong>${escapeHtml(system.short || system.name)}</strong><small>${escapeHtml(system.domain)}</small></span>
      <i class="tab-dot"></i>`;
    button.addEventListener('click', () => selectSystem(index));
    rail.append(button);
  });
  selectSystem(state.activeSystem, false);
}

function selectSystem(index, animate = true) {
  state.activeSystem = index;
  const system = state.profile.systems[index];
  $$('.atlas-tab').forEach((tab, tabIndex) => tab.ariaSelected = String(tabIndex === index));
  const stage = $('#atlas-stage');
  stage.style.setProperty('--stage-accent', system.accent);
  $('#stage-index').textContent = `${String(index + 1).padStart(2, '0')} / ${String(state.profile.systems.length).padStart(2, '0')}`;
  $('#stage-domain').textContent = system.domain.toUpperCase();
  $('#stage-status').innerHTML = `<i></i> ${system.maturity.toUpperCase()}`;
  $('#stage-title').textContent = system.name;
  $('#stage-summary').textContent = system.summary;
  $('#stage-stack').innerHTML = system.stack.map(item => `<span>${escapeHtml(item)}</span>`).join('');
  const proof = SYSTEM_PROOFS[system.id] || [['Status', system.status.toUpperCase()]];
  $('#stage-proof').innerHTML = proof.map(([label, value]) => `<div><small>${escapeHtml(label.toUpperCase())}</small><strong>${escapeHtml(value)}</strong></div>`).join('');
  $('#stage-maturity').textContent = `MATURITY / ${system.maturity.toUpperCase()}`;
  $('#stage-position').textContent = `COORD / ${(index + 1).toFixed(2)}`;
  $('#stage-visual').innerHTML = (SYSTEM_VISUALS[system.id] || SYSTEM_VISUALS.maya)();
  if (animate && state.motion) {
    stage.animate([{ opacity: .65, transform: 'translateY(8px)' }, { opacity: 1, transform: 'translateY(0)' }], { duration: 420, easing: 'cubic-bezier(.16,1,.3,1)' });
  }
}

function renderContinuum() {
  const nav = $('#continuum-nav');
  nav.textContent = '';
  PHASES.forEach((phase, index) => {
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'phase-button';
    button.role = 'tab';
    button.ariaSelected = String(index === state.activePhase);
    button.innerHTML = `<b>${String(index + 1).padStart(2, '0')}</b><span><strong>${phase.title}</strong><small>${phase.subtitle}</small></span>`;
    button.addEventListener('click', () => selectPhase(index));
    nav.append(button);
  });

  const points = PHASES.map((phase, index) => `<circle class="continuum-node${index === 0 ? ' active' : ''}" data-phase-node="${index}" cx="${phase.point[0]}" cy="${phase.point[1]}" r="${index === 0 ? 9 : 6}"/>`).join('');
  $('#continuum-nodes').innerHTML = points;
  selectPhase(0, false);
}

function selectPhase(index, animate = true) {
  state.activePhase = index;
  const phase = PHASES[index];
  $$('.phase-button').forEach((button, buttonIndex) => button.ariaSelected = String(buttonIndex === index));
  $('#phase-index').textContent = `PHASE ${String(index + 1).padStart(2, '0')}`;
  $('#phase-title').textContent = phase.title;
  $('#phase-copy').textContent = phase.copy;
  $('#phase-evidence').innerHTML = phase.evidence.map(([label, value]) => `<div><span>${escapeHtml(label)}</span><strong>${escapeHtml(value)}</strong></div>`).join('');
  const path = $('#continuum-path-live');
  path.style.setProperty('--continuum-offset', phase.offset);
  const cursor = $('#continuum-cursor');
  cursor.setAttribute('cx', phase.point[0]);
  cursor.setAttribute('cy', phase.point[1]);
  $$('[data-phase-node]').forEach((node, nodeIndex) => {
    node.classList.toggle('active', nodeIndex <= index);
    node.setAttribute('r', nodeIndex === index ? '9' : '6');
  });
  if (animate && state.motion) {
    $('.continuum-display').animate([{ opacity: .45, transform: 'translateY(10px)' }, { opacity: 1, transform: 'translateY(0)' }], { duration: 420, easing: 'cubic-bezier(.16,1,.3,1)' });
  }
}

function renderTrip() {
  const states = $('#trip-states');
  states.textContent = '';
  TRIP_STATES.forEach((trip, index) => {
    const button = document.createElement('button');
    button.type = 'button';
    button.className = `trip-state${index === state.activeTrip ? ' active' : ''}`;
    button.innerHTML = `<b>${String(index + 1).padStart(2, '0')}</b><strong>${trip.title}</strong><span></span>`;
    button.addEventListener('click', () => selectTrip(index));
    states.append(button);
  });
  const stops = TRIP_STATES.map((trip, index) => `<circle class="route-stop${index === 0 ? ' active' : ''}" data-route-stop="${index}" cx="${trip.point[0]}" cy="${trip.point[1]}" r="${index === 0 ? 9 : 7}"/>`).join('');
  $('#route-stops').innerHTML = stops;
  selectTrip(0, false);
}

function selectTrip(index, animate = true) {
  state.activeTrip = index;
  const trip = TRIP_STATES[index];
  $$('.trip-state').forEach((button, buttonIndex) => button.classList.toggle('active', buttonIndex === index));
  $('#route-state-label').textContent = trip.title.toUpperCase();
  $('#phone-kicker').textContent = trip.kicker;
  $('#phone-title').textContent = trip.phoneTitle;
  $('#phone-copy').textContent = trip.copy;
  $('#phone-progress').style.setProperty('--trip-progress', `${trip.progress}%`);
  $('#phone-progress').style.width = `${trip.progress}%`;
  $('#route-live').style.setProperty('--route-offset', trip.offset);
  const vehicle = $('#vehicle');
  vehicle.setAttribute('transform', `translate(${trip.point[0]} ${trip.point[1]})`);
  $$('[data-route-stop]').forEach((stop, stopIndex) => {
    stop.classList.toggle('active', stopIndex <= index);
    stop.setAttribute('r', stopIndex === index ? '10' : '7');
  });
  if (animate && state.motion) {
    $('.phone-card').animate([{ opacity: .55, transform: 'translateY(8px)' }, { opacity: 1, transform: 'translateY(0)' }], { duration: 380, easing: 'cubic-bezier(.16,1,.3,1)' });
  }
}

function renderProofCases() {
  const tabs = $('#proof-tabs');
  tabs.textContent = '';
  state.profile.caseStudies.forEach((item, index) => {
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'proof-tab';
    button.role = 'tab';
    button.ariaSelected = String(index === state.activeProof);
    button.innerHTML = `<b>${String(index + 1).padStart(2, '0')}</b><strong>${escapeHtml(item.name)}</strong>`;
    button.addEventListener('click', () => selectProof(index));
    tabs.append(button);
  });
  selectProof(0, false);
}

function selectProof(index, animate = true) {
  state.activeProof = index;
  const item = state.profile.caseStudies[index];
  $$('.proof-tab').forEach((tab, tabIndex) => tab.ariaSelected = String(tabIndex === index));
  const stage = $('#proof-stage');
  stage.innerHTML = `
    <div class="proof-case-title">
      <span>CASE ${String(index + 1).padStart(2, '0')}</span>
      <h3>${escapeHtml(item.name)}</h3>
      <p>${escapeHtml(item.problem)}</p>
    </div>
    <div class="proof-case-body">
      <h4>SYSTEM RESPONSE</h4>
      <p>${escapeHtml(item.system)}</p>
      <div class="proof-receipts">${item.proof.map(value => `<div>${escapeHtml(value)}</div>`).join('')}</div>
    </div>`;
  if (animate && state.motion) {
    stage.animate([{ opacity: .45, transform: 'translateX(10px)' }, { opacity: 1, transform: 'translateX(0)' }], { duration: 420, easing: 'cubic-bezier(.16,1,.3,1)' });
  }
}

function renderMaturity() {
  const shell = $('#maturity-shell');
  shell.innerHTML = `
    <div class="maturity-row header"><span>Capability</span><span>Research</span><span>Prototype</span><span>Integrated</span><span>Verified</span></div>
    ${state.profile.capabilities.map(item => `
      <div class="maturity-row">
        <span>${escapeHtml(item.name)}</span>
        ${['research', 'prototype', 'integrated', 'verified'].map(key => `<span class="maturity-dot${item[key] ? ' on' : ''}" aria-label="${item[key] ? 'Complete' : 'Not complete'}"></span>`).join('')}
      </div>`).join('')}`;
}

function initTheme() {
  let saved = null;
  try { saved = localStorage.getItem('gonzo-apex-theme'); } catch {}
  const initial = saved === 'ivory' || saved === 'obsidian' ? saved : 'obsidian';
  document.documentElement.dataset.theme = initial;
  $('#theme-toggle').addEventListener('click', () => {
    const next = document.documentElement.dataset.theme === 'obsidian' ? 'ivory' : 'obsidian';
    document.documentElement.dataset.theme = next;
    try { localStorage.setItem('gonzo-apex-theme', next); } catch {}
  });
}

function initMotionToggle() {
  const button = $('#motion-toggle');
  const apply = () => {
    document.documentElement.dataset.motion = state.motion ? 'on' : 'off';
    button.ariaPressed = String(state.motion);
    button.textContent = state.motion ? 'MOTION' : 'STILL';
  };
  button.addEventListener('click', () => {
    state.motion = !state.motion;
    apply();
  });
  apply();
}

function initReveals() {
  if (!state.motion) {
    $$('[data-reveal]').forEach(element => element.classList.add('revealed'));
    return;
  }
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('revealed');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: .12, rootMargin: '0px 0px -6% 0px' });
  $$('[data-reveal]').forEach(element => observer.observe(element));
}

function initPointer() {
  if (!matchMedia('(pointer:fine)').matches || !state.motion) return;
  let frame = 0;
  addEventListener('pointermove', event => {
    if (frame) return;
    frame = requestAnimationFrame(() => {
      document.documentElement.style.setProperty('--pointer-x', `${event.clientX}px`);
      document.documentElement.style.setProperty('--pointer-y', `${event.clientY}px`);
      frame = 0;
    });
  }, { passive: true });

  const shell = $('#world-shell');
  shell.addEventListener('pointermove', event => {
    const rect = shell.getBoundingClientRect();
    const x = (event.clientX - rect.left) / rect.width - .5;
    const y = (event.clientY - rect.top) / rect.height - .5;
    shell.style.transform = `perspective(1100px) rotateX(${(-y * 3.8).toFixed(2)}deg) rotateY(${(x * 4.8).toFixed(2)}deg)`;
  }, { passive: true });
  shell.addEventListener('pointerleave', () => { shell.style.transform = ''; });
}

function initWorldCanvas() {
  const canvas = $('#world-canvas');
  const context = canvas.getContext('2d', { alpha: true });
  if (!context || !state.motion) return;
  let width = 0;
  let height = 0;
  let dpr = 1;
  let nodes = [];
  let raf = 0;
  let visible = true;
  const pointer = { x: -1000, y: -1000 };

  const resize = () => {
    width = innerWidth;
    height = innerHeight;
    dpr = Math.min(devicePixelRatio || 1, 1.6);
    canvas.width = Math.floor(width * dpr);
    canvas.height = Math.floor(height * dpr);
    canvas.style.width = `${width}px`;
    canvas.style.height = `${height}px`;
    context.setTransform(dpr, 0, 0, dpr, 0, 0);
    const count = Math.max(24, Math.min(78, Math.floor((width * height) / 26000)));
    nodes = Array.from({ length: count }, (_, index) => ({
      x: Math.random() * width,
      y: Math.random() * height,
      vx: (Math.random() - .5) * .16,
      vy: (Math.random() - .5) * .16,
      size: index % 8 === 0 ? 1.7 : .9,
    }));
  };

  const draw = () => {
    raf = 0;
    if (!visible || !state.motion) return;
    context.clearRect(0, 0, width, height);
    const accent = getComputedStyle(document.documentElement).getPropertyValue('--teal').trim() || '#2ad7b5';
    context.fillStyle = accent;
    context.strokeStyle = accent;

    for (let index = 0; index < nodes.length; index++) {
      const node = nodes[index];
      node.x += node.vx;
      node.y += node.vy;
      if (node.x < -30) node.x = width + 30;
      if (node.x > width + 30) node.x = -30;
      if (node.y < -30) node.y = height + 30;
      if (node.y > height + 30) node.y = -30;

      const dxPointer = pointer.x - node.x;
      const dyPointer = pointer.y - node.y;
      const pointerDistance = Math.hypot(dxPointer, dyPointer);
      if (pointerDistance < 170 && pointerDistance > 0) {
        node.x -= (dxPointer / pointerDistance) * .11;
        node.y -= (dyPointer / pointerDistance) * .11;
      }

      context.globalAlpha = .24;
      context.beginPath();
      context.arc(node.x, node.y, node.size, 0, Math.PI * 2);
      context.fill();

      for (let otherIndex = index + 1; otherIndex < nodes.length; otherIndex++) {
        const other = nodes[otherIndex];
        const dx = node.x - other.x;
        const dy = node.y - other.y;
        const distance = Math.hypot(dx, dy);
        if (distance < 142) {
          context.globalAlpha = (1 - distance / 142) * .07;
          context.beginPath();
          context.moveTo(node.x, node.y);
          context.lineTo(other.x, other.y);
          context.stroke();
        }
      }
    }
    context.globalAlpha = 1;
    raf = requestAnimationFrame(draw);
  };

  addEventListener('resize', resize, { passive: true });
  addEventListener('pointermove', event => { pointer.x = event.clientX; pointer.y = event.clientY; }, { passive: true });
  document.addEventListener('visibilitychange', () => {
    visible = !document.hidden;
    if (!visible && raf) cancelAnimationFrame(raf);
    if (visible && !raf) raf = requestAnimationFrame(draw);
  });
  resize();
  raf = requestAnimationFrame(draw);
}

function initClock() {
  const formatter = new Intl.DateTimeFormat('en-GB', {
    timeZone: 'Europe/Sofia', hour: '2-digit', minute: '2-digit', second: '2-digit',
  });
  const update = () => { $('#sofia-time').textContent = formatter.format(new Date()); };
  update();
  setInterval(update, 1000);
}

function initLabCanvases() {
  initAudioCanvas();
  initRfCanvas();
}

function initAudioCanvas() {
  const canvas = $('#audio-canvas');
  const context = canvas.getContext('2d');
  if (!context) return;
  let width = 0;
  let height = 0;
  let phase = 0;
  let raf = 0;

  const resize = () => {
    const rect = canvas.getBoundingClientRect();
    const dpr = Math.min(devicePixelRatio || 1, 1.5);
    width = rect.width;
    height = rect.height;
    canvas.width = Math.floor(width * dpr);
    canvas.height = Math.floor(height * dpr);
    context.setTransform(dpr, 0, 0, dpr, 0, 0);
  };

  const draw = () => {
    raf = 0;
    context.clearRect(0, 0, width, height);
    const color = getComputedStyle(document.documentElement).getPropertyValue('--violet').trim() || '#b79cff';
    const line = getComputedStyle(document.documentElement).getPropertyValue('--line').trim() || 'rgba(255,255,255,.1)';
    context.strokeStyle = line;
    context.lineWidth = 1;
    for (let y = 40; y < height; y += 40) {
      context.beginPath(); context.moveTo(0, y); context.lineTo(width, y); context.stroke();
    }
    for (let layer = 0; layer < 3; layer++) {
      context.beginPath();
      context.strokeStyle = color;
      context.globalAlpha = .8 - layer * .22;
      context.lineWidth = 1.5 + layer * .5;
      for (let x = 0; x <= width; x += 3) {
        const t = x / width;
        const envelope = Math.sin(Math.PI * t) ** 1.2;
        const y = height * .45
          + Math.sin(t * Math.PI * (9 + layer * 2) + phase * (1 + layer * .08)) * 42 * envelope
          + Math.sin(t * Math.PI * 28 - phase * .7) * 13 * envelope;
        if (x === 0) context.moveTo(x, y); else context.lineTo(x, y);
      }
      context.stroke();
    }
    context.globalAlpha = 1;
    phase += state.motion ? .022 : 0;
    raf = requestAnimationFrame(draw);
  };

  new ResizeObserver(resize).observe(canvas);
  resize();
  raf = requestAnimationFrame(draw);
}

function initRfCanvas() {
  const canvas = $('#rf-canvas');
  const context = canvas.getContext('2d');
  if (!context) return;
  let width = 0;
  let height = 0;
  let angle = 0;
  const targets = [
    { x: .68, y: .35, strength: .82 },
    { x: .34, y: .63, strength: .55 },
    { x: .77, y: .69, strength: .38 },
  ];

  const resize = () => {
    const rect = canvas.getBoundingClientRect();
    const dpr = Math.min(devicePixelRatio || 1, 1.5);
    width = rect.width;
    height = rect.height;
    canvas.width = Math.floor(width * dpr);
    canvas.height = Math.floor(height * dpr);
    context.setTransform(dpr, 0, 0, dpr, 0, 0);
  };

  const draw = () => {
    context.clearRect(0, 0, width, height);
    const accent = getComputedStyle(document.documentElement).getPropertyValue('--blue').trim() || '#75baff';
    const line = getComputedStyle(document.documentElement).getPropertyValue('--line').trim() || 'rgba(255,255,255,.1)';
    const cx = width / 2;
    const cy = height / 2;
    const radius = Math.min(width, height) * .34;
    context.strokeStyle = line;
    context.lineWidth = 1;
    for (let ring = 1; ring <= 4; ring++) {
      context.beginPath(); context.arc(cx, cy, radius * ring / 4, 0, Math.PI * 2); context.stroke();
    }
    context.beginPath(); context.moveTo(cx - radius, cy); context.lineTo(cx + radius, cy); context.moveTo(cx, cy - radius); context.lineTo(cx, cy + radius); context.stroke();

    const gradient = context.createLinearGradient(cx, cy, cx + Math.cos(angle) * radius, cy + Math.sin(angle) * radius);
    gradient.addColorStop(0, accent);
    gradient.addColorStop(1, 'transparent');
    context.strokeStyle = gradient;
    context.lineWidth = 2;
    context.beginPath(); context.moveTo(cx, cy); context.lineTo(cx + Math.cos(angle) * radius, cy + Math.sin(angle) * radius); context.stroke();

    targets.forEach(target => {
      const x = width * target.x;
      const y = height * target.y;
      context.globalAlpha = .35 + target.strength * .6;
      context.fillStyle = accent;
      context.beginPath(); context.arc(x, y, 3 + target.strength * 4, 0, Math.PI * 2); context.fill();
      context.globalAlpha = .12;
      context.beginPath(); context.arc(x, y, 16 + target.strength * 18, 0, Math.PI * 2); context.fill();
    });
    context.globalAlpha = 1;
    angle += state.motion ? .008 : 0;
    requestAnimationFrame(draw);
  };

  new ResizeObserver(resize).observe(canvas);
  resize();
  requestAnimationFrame(draw);
}

function sha256Fallback(value) {
  const ascii = unescape(encodeURIComponent(value));
  const maxWord = Math.pow(2, 32);
  let result = '';
  const words = [];
  const bitLength = ascii.length * 8;
  const hash = [];
  const constants = [];
  const composite = {};
  let primeCount = 0;

  for (let candidate = 2; primeCount < 64; candidate++) {
    if (composite[candidate]) continue;
    for (let multiple = candidate * candidate; multiple < 313; multiple += candidate) composite[multiple] = true;
    hash[primeCount] = (Math.pow(candidate, .5) * maxWord) | 0;
    constants[primeCount] = (Math.pow(candidate, 1 / 3) * maxWord) | 0;
    primeCount++;
  }

  let padded = `${ascii}\x80`;
  while (padded.length % 64 !== 56) padded += '\x00';
  for (let index = 0; index < padded.length; index++) {
    words[index >> 2] |= padded.charCodeAt(index) << ((3 - index) % 4) * 8;
  }
  words.push((bitLength / maxWord) | 0, bitLength | 0);

  for (let chunk = 0; chunk < words.length; chunk += 16) {
    const schedule = words.slice(chunk, chunk + 16);
    const oldHash = hash.slice(0, 8);
    let working = hash.slice(0, 8);

    for (let round = 0; round < 64; round++) {
      const w15 = schedule[round - 15];
      const w2 = schedule[round - 2];
      const a = working[0];
      const e = working[4];
      const sigma0 = round < 16 ? 0 : ((w15 >>> 7) | (w15 << 25)) ^ ((w15 >>> 18) | (w15 << 14)) ^ (w15 >>> 3);
      const sigma1 = round < 16 ? 0 : ((w2 >>> 17) | (w2 << 15)) ^ ((w2 >>> 19) | (w2 << 13)) ^ (w2 >>> 10);
      schedule[round] = round < 16 ? schedule[round] : (schedule[round - 16] + sigma0 + schedule[round - 7] + sigma1) | 0;
      const sum1 = ((e >>> 6) | (e << 26)) ^ ((e >>> 11) | (e << 21)) ^ ((e >>> 25) | (e << 7));
      const choice = (e & working[5]) ^ (~e & working[6]);
      const temp1 = (working[7] + sum1 + choice + constants[round] + schedule[round]) | 0;
      const sum0 = ((a >>> 2) | (a << 30)) ^ ((a >>> 13) | (a << 19)) ^ ((a >>> 22) | (a << 10));
      const majority = (a & working[1]) ^ (a & working[2]) ^ (working[1] & working[2]);
      const temp2 = (sum0 + majority) | 0;
      working = [(temp1 + temp2) | 0, working[0], working[1], working[2], (working[3] + temp1) | 0, working[4], working[5], working[6]];
    }

    for (let index = 0; index < 8; index++) hash[index] = (oldHash[index] + working[index]) | 0;
  }

  for (let index = 0; index < 8; index++) {
    for (let byte = 3; byte >= 0; byte--) {
      const valueByte = (hash[index] >>> (byte * 8)) & 255;
      result += valueByte.toString(16).padStart(2, '0');
    }
  }
  return result;
}

async function sha256(value) {
  if (globalThis.crypto?.subtle) {
    const data = new TextEncoder().encode(value);
    const digest = await globalThis.crypto.subtle.digest('SHA-256', data);
    return [...new Uint8Array(digest)].map(byte => byte.toString(16).padStart(2, '0')).join('');
  }
  return sha256Fallback(value);
}

async function buildLedger({ preserveMutation = false } = {}) {
  const basePayloads = ['operator-intent', 'policy-approved', 'workspace-action', 'verification-pass', 'receipt-issued'];
  const payloads = preserveMutation && state.ledger.length ? state.ledger.map(block => block.payload) : basePayloads;
  state.ledger = [];
  let previous = 'GENESIS';
  for (let index = 0; index < payloads.length; index++) {
    const payload = payloads[index];
    const hash = await sha256(`${index}|${payload}|${previous}`);
    state.ledger.push({ index, payload, previous, hash, valid: true });
    previous = hash;
  }
  await buildMerkle();
  renderLedger();
}

async function buildMerkle() {
  let layer = state.ledger.map(block => ({ hash: block.hash, children: [block.index], valid: block.valid }));
  const layers = [layer];
  while (layer.length > 1) {
    const next = [];
    for (let index = 0; index < layer.length; index += 2) {
      const left = layer[index];
      const right = layer[index + 1] || left;
      next.push({
        hash: await sha256(`${left.hash}|${right.hash}`),
        children: [...new Set([...left.children, ...right.children])],
        valid: left.valid && right.valid,
      });
    }
    layer = next;
    layers.push(layer);
  }
  state.merkle = layers;
}

function renderLedger() {
  const svgLinks = $('#merkle-links');
  const svgNodes = $('#merkle-nodes');
  svgLinks.textContent = '';
  svgNodes.textContent = '';

  const leafX = [120, 340, 560, 780, 1000];
  const leafY = 420;
  const middleY = 270;
  const upperY = 150;
  const rootY = 55;

  const positions = [];
  positions[0] = state.ledger.map((_, index) => ({ x: leafX[index], y: leafY }));
  positions[1] = [{ x: 230, y: middleY }, { x: 670, y: middleY }, { x: 1000, y: middleY }];
  positions[2] = [{ x: 450, y: upperY }, { x: 1000, y: upperY }];
  positions[3] = [{ x: 725, y: rootY }];

  for (let layerIndex = 1; layerIndex < state.merkle.length; layerIndex++) {
    state.merkle[layerIndex].forEach((node, nodeIndex) => {
      const parent = positions[layerIndex][nodeIndex];
      const childA = positions[layerIndex - 1][nodeIndex * 2];
      const childB = positions[layerIndex - 1][nodeIndex * 2 + 1] || childA;
      [childA, childB].forEach(child => {
        const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        path.setAttribute('d', `M${child.x} ${child.y - 32}C${child.x} ${child.y - 90},${parent.x} ${parent.y + 90},${parent.x} ${parent.y + 32}`);
        path.setAttribute('class', `merkle-link ${node.valid ? 'live' : 'invalid'}`);
        svgLinks.append(path);
      });
    });
  }

  state.merkle.forEach((layer, layerIndex) => {
    layer.forEach((node, nodeIndex) => {
      const position = positions[layerIndex][nodeIndex];
      const group = document.createElementNS('http://www.w3.org/2000/svg', 'g');
      group.setAttribute('class', `merkle-node ${node.valid ? 'valid' : 'invalid'}`);
      group.setAttribute('transform', `translate(${position.x - 70} ${position.y - 30})`);
      group.innerHTML = `<rect width="140" height="60"></rect><text x="70" y="25">${layerIndex === 0 ? `R${String(nodeIndex + 1).padStart(2, '0')}` : layerIndex === state.merkle.length - 1 ? 'MERKLE ROOT' : `AGG ${layerIndex}.${nodeIndex + 1}`}</text><text class="hash" x="70" y="43">${node.hash.slice(0, 10)}…</text>`;
      svgNodes.append(group);
    });
  });

  $('#receipt-strip').innerHTML = state.ledger.map(block => `<div class="receipt-chip${block.valid ? '' : ' invalid'}"><small>RECEIPT ${String(block.index + 1).padStart(2, '0')}</small><strong>${block.hash.slice(0, 18)}…</strong></div>`).join('');
  const root = state.merkle.at(-1)?.[0];
  $('#merkle-root').textContent = `ROOT / ${root ? `${root.hash.slice(0, 18)}…${root.hash.slice(-8)}` : 'UNAVAILABLE'}`;
  const allValid = state.ledger.every(block => block.valid) && root?.valid;
  const status = $('#ledger-state');
  status.className = `ledger-state ${allValid ? 'valid' : 'invalid'}`;
  status.innerHTML = `<i></i> ${allValid ? 'PROOF FABRIC VALID' : 'MUTATION DETECTED'}`;
}

async function tamperLedger() {
  if (!state.ledger.length) return;
  const target = state.ledger[2];
  target.payload = target.payload.includes('MUTATED') ? 'workspace-action' : 'workspace-action::MUTATED';
  target.valid = false;
  for (let index = target.index + 1; index < state.ledger.length; index++) state.ledger[index].valid = false;
  await buildMerkle();
  renderLedger();
}

async function repairLedger() {
  await buildLedger();
  if (state.motion) {
    $('.ledger-world').animate([{ opacity: .45, transform: 'scale(.992)' }, { opacity: 1, transform: 'scale(1)' }], { duration: 480, easing: 'cubic-bezier(.16,1,.3,1)' });
  }
}

function initAutoScenes() {
  let phaseTimer = 0;
  let tripTimer = 0;
  const schedule = () => {
    clearInterval(phaseTimer);
    clearInterval(tripTimer);
    if (!state.motion) return;
    phaseTimer = setInterval(() => {
      if (!document.hidden && isSectionVisible('#maya')) selectPhase((state.activePhase + 1) % PHASES.length);
    }, 4200);
    tripTimer = setInterval(() => {
      if (!document.hidden && isSectionVisible('#mobility')) selectTrip((state.activeTrip + 1) % TRIP_STATES.length);
    }, 3600);
  };
  $('#motion-toggle').addEventListener('click', schedule);
  schedule();
}

function isSectionVisible(selector) {
  const element = $(selector);
  const rect = element.getBoundingClientRect();
  return rect.top < innerHeight * .82 && rect.bottom > innerHeight * .18;
}

function registerServiceWorker() {
  if ('serviceWorker' in navigator && location.protocol === 'https:') {
    navigator.serviceWorker.register('./sw.js').catch(() => {});
  }
}

async function main() {
  initTheme();
  initMotionToggle();
  initClock();
  renderContinuum();
  renderTrip();
  initReveals();
  initPointer();
  initWorldCanvas();
  initLabCanvases();
  await Promise.all([loadProfile(), buildLedger()]);
  $('#tamper-ledger').addEventListener('click', tamperLedger);
  $('#repair-ledger').addEventListener('click', repairLedger);
  initAutoScenes();
  registerServiceWorker();
}

main().catch(error => {
  console.error(error);
  document.documentElement.dataset.runtimeFault = 'true';
});
