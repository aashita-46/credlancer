// beginner-friendly JS: connect wallet, create gig, deposit, mint badges
const API = "http://127.0.0.1:5000"; // backend must run here
let walletAddress = null;

// Replace these placeholders with real addresses after publishing
const ESCROW_ADDR = "0xESCROW_ADDRESS";       // escrow account to receive deposits
const MODULE_SKILL = "0xMODULE_SKILL_ADDR";   // SkillBadge module address
const MODULE_MENTOR = "0xMODULE_MENTOR_ADDR"; // MentorBadge module address

// UI elements
const connectBtn = document.getElementById('connectBtn');
const addrDiv = document.getElementById('addr');
const createGigBtn = document.getElementById('createGigBtn');
const depositBtn = document.getElementById('depositBtn');
const viewBadgesBtn = document.getElementById('viewBadgesBtn');
const mintSkillBtn = document.getElementById('mintSkillBtn');
const mintMentorBtn = document.getElementById('mintMentorBtn');
const amountInput = document.getElementById('amountInput');
const statusPre = document.getElementById('status');

function setStatus(s){ statusPre.textContent = "Status: " + s; }
function showAddr(a){ addrDiv.textContent = a.slice(0,10) + "..." + a.slice(-6); }

// connect to Petra / Aptos wallet
connectBtn.onclick = async () => {
  if (!window.aptos) { alert("Please install Petra wallet (Chrome/Edge) and refresh."); return; }
  try {
    const resp = await window.aptos.connect();
    walletAddress = resp.address;
    showAddr(walletAddress);
    setStatus("Connected wallet");
  } catch (e) {
    console.error(e); setStatus("Wallet connect failed");
  }
};

// create a demo gig (calls backend)
createGigBtn.onclick = async () => {
  if (!walletAddress) return alert("Connect your wallet first");
  const body = { title: "Landing page design", budget: 1.5, skills: ["html","css","js"], client: walletAddress };
  const r = await fetch(`${API}/api/gigs`, { method: "POST", headers:{'content-type':'application/json'}, body: JSON.stringify(body)});
  const data = await r.json();
  setStatus("Created gig id: " + data.id);
};

// deposit to escrow (wallet signs transfer)
depositBtn.onclick = async () => {
  if (!walletAddress) return alert("Connect your wallet first");
  // read amount (APT) and convert to Octas (1 APT = 100_000_000 octas)
  const input = amountInput.value || "0.001";
  const apt = parseFloat(input);
  if (isNaN(apt) || apt <= 0) return alert("Enter amount in APT, e.g., 0.001");
  const octas = Math.round(apt * 100000000).toString();

  const payload = {
    type: "entry_function_payload",
    function: "0x1::coin::transfer",
    type_arguments: ["0x1::aptos_coin::AptosCoin"],
    arguments: [ESCROW_ADDR, octas]
  };

  try {
    setStatus("Prompting wallet to send deposit...");
    const tx = await window.aptos.signAndSubmitTransaction(payload);
    setStatus("Deposit tx submitted: " + tx.hash);
    // For demo we assume gig id 1; in real app pass actual gig id
    await fetch(`${API}/api/gigs/1/deposit`, { method: "POST", headers:{'content-type':'application/json'}, body: JSON.stringify({tx_hash: tx.hash})});
    setStatus("Deposit recorded in backend");
  } catch (e) {
    console.error(e); setStatus("Deposit failed");
  }
};

// view badges (calls backend to show locally-recorded badges)
viewBadgesBtn.onclick = async () => {
  if (!walletAddress) return alert("Connect your wallet first");
  const r = await fetch(`${API}/api/badges?owner=${walletAddress}`);
  const arr = await r.json();
  if (!arr || arr.length === 0) setStatus("No badges recorded locally");
  else setStatus("Badges: " + JSON.stringify(arr, null, 2));
};

// simple admin mint (should be run by admin wallet that published modules)
mintSkillBtn.onclick = async () => {
  if (!walletAddress) return alert("Connect wallet (admin) first");
  const project = "Demo Project";
  const nameBytes = Array.from(new TextEncoder().encode("Badge-"+project));
  const descBytes = Array.from(new TextEncoder().encode("Completed: "+project));
  const uriBytes = Array.from(new TextEncoder().encode("https://example.com/badge.png"));

  const payload = {
    type: "entry_function_payload",
    function: `${MODULE_SKILL}::SkillBadge::mint_skill_badge`,
    type_arguments: [],
    arguments: [walletAddress, nameBytes, descBytes, uriBytes]
  };

  try {
    setStatus("Requesting mint...");
    const tx = await window.aptos.signAndSubmitTransaction(payload);
    setStatus("Mint tx: " + tx.hash);
    // record mint in backend
    await fetch(`${API}/api/admin/record_badge`, { method: "POST", headers:{'content-type':'application/json'}, body: JSON.stringify({owner: walletAddress, badge_type:"skill", tx: tx.hash, metadata:project})});
  } catch (e) {
    console.error(e); setStatus("Mint failed");
  }
};

mintMentorBtn.onclick = async () => {
  if (!walletAddress) return alert("Connect wallet (admin) first");
  const mentorName = "Mentor Verified";
  const nameBytes = Array.from(new TextEncoder().encode("Mentor-"+mentorName));
  const descBytes = Array.from(new TextEncoder().encode("Verified mentor"));
  const uriBytes = Array.from(new TextEncoder().encode("https://example.com/mentor.png"));

  const payload = {
    type: "entry_function_payload",
    function: `${MODULE_MENTOR}::MentorBadge::mint_mentor_badge`,
    type_arguments: [],
    arguments: [walletAddress, nameBytes, descBytes, uriBytes]
  };

  try {
    setStatus("Requesting mentor badge mint...");
    const tx = await window.aptos.signAndSubmitTransaction(payload);
    setStatus("Mentor mint tx: " + tx.hash);
    await fetch(`${API}/api/admin/record_badge`, { method: "POST", headers:{'content-type':'application/json'}, body: JSON.stringify({owner: walletAddress, badge_type:"mentor", tx: tx.hash, metadata:mentorName})});
  } catch (e) {
    console.error(e); setStatus("Mentor mint failed");
  }
};
