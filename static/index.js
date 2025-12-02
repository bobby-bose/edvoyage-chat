let conversationsData = [];
let allUsersData = [];
let mergedList = [];
const params = new URLSearchParams(location.search);
const currentEmail = params.get('email');
async function loadConversations(){
  // server will use settings.STATIC_CURRENT_USER_EMAIL if client omits email
  const res = await fetch(`/api/conversations`);
  const data = await res.json();
  conversationsData = data.conversations || [];
  await loadAllUsers();
  mergeAndRender();
}

async function loadAllUsers(){
  const res = await fetch(`/api/users`);
  const data = await res.json();
  allUsersData = data.users || [];
}

function mergeAndRender(){
  // Get emails of users we already have conversations with
  const conversationEmails = new Set(conversationsData.map(c => c.other_email));
  
  // Find users we haven't chatted with yet
  const newUsers = allUsersData.filter(u => !conversationEmails.has(u.email));
  
  // Merge: active conversations first (sorted by time DESC), then new users (sorted by email)
  mergedList = [
    ...conversationsData,
    ...newUsers.map(u => ({
      other_email: u.email,
      other_name: u.name,
      last_text: '',
      last_time: '',
      unread: 0,
      is_new: true
    }))
  ];
  
  renderConversations(mergedList);
}

function renderConversations(list){
  const container = document.getElementById('conversationList');
  container.innerHTML='';
  list.forEach(c=>{
    const d = document.createElement('div');
    d.className='conv-row';
    if(c.is_new){
      d.innerHTML = `<div class="conv-main"><strong>${c.other_name||c.other_email}</strong><div class="preview">No messages yet</div></div><div class="conv-meta"><div class="time"></div><div class="unread"></div></div>`;
    } else {
      d.innerHTML = `<div class="conv-main"><strong>${c.other_name||c.other_email}</strong><div class="preview">${c.last_text}</div></div><div class="conv-meta"><div class="time">${new Date(c.last_time).toLocaleString()}</div><div class="unread">${c.unread}</div></div>`;
    }
    d.addEventListener('click', ()=>{
      location.href = `/chat/?email=${encodeURIComponent(currentEmail)}&other_email=${encodeURIComponent(c.other_email)}`;
    });
    container.appendChild(d);
  })
}

// Live search on keyup
document.getElementById('searchInput').addEventListener('input', (e)=>{
  // filter on every change (letter added or removed) - word by word
  const q = e.target.value.trim().toLowerCase();
  if(!q) return renderConversations(mergedList);
  const filtered = mergedList.filter(c=>{
    return (c.other_email||'').toLowerCase().includes(q) || (c.other_name||'').toLowerCase().includes(q) || (c.last_text||'').toLowerCase().includes(q);
  });
  renderConversations(filtered);
});

// Load on page ready
document.addEventListener('DOMContentLoaded', ()=>{
  loadConversations();
});
