const params = new URLSearchParams(location.search);
const otherEmail = params.get('other_email');
const currentEmail = params.get('email');
const messageBox = document.getElementById('messageBox');

// update header displays if present. The server provides the current user email
const otherDisplayEl = document.getElementById('otherDisplay');
const currentDisplayEl = document.getElementById('currentDisplay');
if(otherDisplayEl) otherDisplayEl.textContent = otherEmail || '';

const backBtn = document.getElementById('backBtn');
if(backBtn) backBtn.addEventListener('click', ()=>{ location.href = '/'; });


async function fetchMessages(){
  if(!otherEmail) return;
  // omit the email param so server uses settings.STATIC_CURRENT_USER_EMAIL
  const res = await fetch(`/api/messages?email=${encodeURIComponent(currentEmail)}&other_email=${encodeURIComponent(otherEmail)}`);
  const data = await res.json();
  if(!data.messages) return;
  messageBox.innerHTML = '';
  data.messages.forEach(m=>{
    const row = document.createElement('div');
    row.className='msg-row';
      // Normalize emails and show messages from the other user on the LEFT, and current user's on the RIGHT
      const senderEmail = (m.sender || '').toLowerCase().trim();
      const otherNormalized = (otherEmail || '').toLowerCase().trim();
      const isOther = senderEmail === otherNormalized;
      const bubble = document.createElement('div');
      bubble.className = isOther ? 'msg-left' : 'msg-right';

    const time = new Date(m.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
console.log(time);

    bubble.innerHTML = `<div class="msg-text">${m.text||''}</div>` + (m.image_url?`<img src="${m.image_url}" class="chat-image">`:'') + `<div class="timestamp">${time} <span class="tick ${m.seen? 'seen':''}">${m.seen? '✓✓': (m.delivered? '✓✓':'✓')}</span></div>`;
    row.appendChild(bubble);
    messageBox.appendChild(row);
  })
  messageBox.scrollTop = messageBox.scrollHeight;
}

setInterval(fetchMessages,2000);
fetchMessages();

document.getElementById('attachBtn').addEventListener('click', ()=>document.getElementById('imageInput').click());
document.getElementById('sendBtn').addEventListener('click', async ()=>{
  const text = document.getElementById('textInput').value;
  const input = document.getElementById('imageInput');
  const fd = new FormData();
  // do not send from_email; server will use STATIC_CURRENT_USER_EMAIL when missing
  fd.append('to_email', otherEmail);
  if(text) fd.append('text', text);
  if(input.files[0]) fd.append('image', input.files[0]);
  const res = await fetch('/api/send', {method:'POST', body:fd});
  const data = await res.json();
  document.getElementById('textInput').value='';
  input.value='';
  fetchMessages();
});
