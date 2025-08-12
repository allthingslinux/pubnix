"""Minimal HTML pages for application form and admin review."""

from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from sqlmodel import Session

from database import get_session

router = APIRouter(tags=["web"])


@router.get("/apply", response_class=HTMLResponse)
async def application_form() -> str:
    return """
        <html>
          <head><title>ATL Pubnix Application</title></head>
          <body>
            <h1>Apply for ATL Pubnix</h1>
            <form method="post" action="/api/v1/applications/" onsubmit="return submitForm(event)">
              <label>Email <input type="email" name="email" required /></label><br />
              <label>Requested Username <input type="text" name="username_requested" required /></label><br />
              <label>Full Name <input type="text" name="full_name" required /></label><br />
              <label>Motivation <textarea name="motivation"></textarea></label><br />
              <label><input type="checkbox" name="community_guidelines_accepted" required /> I accept community guidelines</label><br />
              <button type="submit">Submit</button>
            </form>
            <pre id="result"></pre>
            <script>
            async function submitForm(e){
              e.preventDefault();
              const form = e.target;
              const payload = {
                email: form.email.value,
                username_requested: form.username_requested.value,
                full_name: form.full_name.value,
                motivation: form.motivation.value,
                community_guidelines_accepted: form.community_guidelines_accepted.checked
              };
              const res = await fetch(form.action, {method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify(payload)});
              const data = await res.json();
              document.getElementById('result').textContent = JSON.stringify(data, null, 2);
            }
            </script>
          </body>
        </html>
        """


@router.get("/admin/review", response_class=HTMLResponse)
async def admin_review_page(session: Session = Depends(get_session)) -> str:
    # lightweight page that fetches applications via API
    return """
        <html>
          <head><title>ATL Pubnix Admin Review</title></head>
          <body>
            <h1>Pending Applications</h1>
            <div id="apps"></div>
            <script>
            async function load(){
              const res = await fetch('/api/v1/applications/?limit=50');
              const apps = await res.json();
              const container = document.getElementById('apps');
              container.innerHTML = '';
              apps.filter(a => a.status === 'pending').forEach(a => {
                const div = document.createElement('div');
                div.style.border = '1px solid #ccc';
                div.style.margin = '8px';
                div.style.padding = '8px';
                div.innerHTML = `<strong>#${a.id}</strong> ${a.full_name} &lt;${a.email}&gt; requested <code>${a.username_requested}</code>
                  <br/><button onclick="review(${a.id}, 'approved')">Approve</button>
                  <button onclick="review(${a.id}, 'rejected')">Reject</button>`;
                container.appendChild(div);
              });
            }
            async function review(id, status){
              const res = await fetch(`/api/v1/applications/${id}/review`, {method:'PATCH', headers:{'Content-Type':'application/json'}, body: JSON.stringify({status, review_notes: status==='approved'?'Approved via admin page':''})});
              await res.json();
              await load();
            }
            load();
            </script>
          </body>
        </html>
        """
