"""
eSub Studio Enterprise — Local Hybrid AI Edition
Single-file Streamlit application. Run: streamlit run app.py
Optional dependencies: streamlit, requests, pypdf, PyYAML, openai, google-generativeai.
Secrets are session-only unless supplied through environment variables.
"""
from __future__ import annotations
import os, re, json, time, uuid, hashlib, hmac, secrets, sqlite3, random, io, datetime, traceback
from pathlib import Path
from typing import Any

try:
    import streamlit as st
except ImportError:
    raise SystemExit("Install Streamlit first: pip install streamlit")

APP = "eSub Studio Enterprise"
DB_PATH = Path(os.getenv("ESUB_DB_PATH", "esub_studio.db"))
PALETTES = {
    "Coral Bloom": "#FF7F70", "Ocean Teal": "#14B8A6", "Sapphire": "#3973D6",
    "Amethyst": "#9B72CF", "Citrus": "#C4A000", "Forest": "#39845A",
    "Rose Quartz": "#D77A9B", "Arctic": "#4F9CC8", "Graphite": "#7C8798", "Solar": "#E18A28"
}
I18N = {
"zh-TW": {"home":"總覽儀表板","notes":"AI 筆記管家","prompt":"範本／提示詞工作區","fill":"填表代理","skills":"技能／代理工作區","pipeline":"流程工作區","results":"成果／下載中心","notifications":"通知中心","account":"帳戶／個人資料","settings":"設定／系統偏好","logs":"診斷／執行紀錄","provider":"模型供應商","model":"模型","run":"執行 AI","input":"輸入內容","output":"輸出結果","save":"儲存","language":"語言","theme":"主題","palette":"色彩風格","local":"本機端點","api":"API 金鑰","guest":"訪客模式","warning":"注意","success":"成功","error":"錯誤"},
"en": {"home":"WOW Dashboard","notes":"AI Note Keeper","prompt":"Template / Prompt Workspace","fill":"Fill Agent","skills":"Skill / Agent Workspace","pipeline":"Pipeline Workspace","results":"Results / Downloads","notifications":"Notifications","account":"Account / Profile","settings":"Settings","logs":"Diagnostics / Execution Viewer","provider":"Provider","model":"Model","run":"Run AI","input":"Input","output":"Output","save":"Save","language":"Language","theme":"Theme","palette":"Palette","local":"Local endpoint","api":"API key","guest":"Guest mode","warning":"Warning","success":"Success","error":"Error"},
"ja": {"home":"ダッシュボード","notes":"AIノート","prompt":"テンプレート／プロンプト","fill":"入力エージェント","skills":"スキル／エージェント","pipeline":"パイプライン","results":"成果／ダウンロード","notifications":"通知","account":"アカウント","settings":"設定","logs":"診断／実行ログ","provider":"プロバイダー","model":"モデル","run":"AIを実行","input":"入力","output":"出力","save":"保存","language":"言語","theme":"テーマ","palette":"配色","local":"ローカル接続先","api":"APIキー","guest":"ゲストモード","warning":"注意","success":"成功","error":"エラー"}
}
WOW = [
("Live Execution Pulse","即時顯示階段、耗時、供應商、模型與最近事件。","以真實執行事件更新，避免裝飾性假狀態。"),
("Token Budget Sentinel","估算輸入／輸出 token，監測工作階段用量。","估算值明確標示；供應商用量缺失時不冒充精確值。"),
("Quick Route Genius","依任務文字提示合適模組與本機／雲端路由。","提供建議，不擅自切換模型。"),
("Consistency Cross-Checker","找出文件中的矛盾、重複與版本差異。","結果作為待審查提示，不自動改寫原文。"),
("Template Migration Assistant","將內容映射到新模板並標示不確定欄位。","適合版本遷移；需人工確認。"),
("Public Release Redaction Assistant","標記疑似個資、憑證或機密供遮蔽審查。","僅提出候選遮蔽，不宣稱法律合規。"),
("Prompt Comparator","同一輸入比較兩種提示或模型輸出。","支援迭代評估；可能產生額外 API 費用。"),
("Source-to-Claim Traceboard","將生成內容與原始段落建立引用線索。","無來源時明確標示未追溯。"),
("Session Recovery Oracle","提供重載前已保留的工作階段內容與復原提示。","本版採 session state；不保證跨瀏覽器持久復原。"),
("Insight Burst","依目前文字提供摘要、行動項目、改寫等快捷操作。","需使用者點擊才執行。")
]
MAGICS = ["AI Keywords","Smart Summarizer","Structure Refiner","Action Extractor","Terminology Explainer","Rewrite Lens"]
def tr(k): return I18N.get(st.session_state.get("locale","zh-TW"), I18N["zh-TW"]).get(k,k)
def init_state():
    defaults={"locale":"zh-TW","theme":"Dark","palette":"Coral Bloom","page":"home","provider":"Local OpenAI-compatible","model":"gemma-4-31b-it","local_url":os.getenv("LOCAL_LLM_BASE_URL","http://127.0.0.1:11434"),"local_token":"","gemini_key":"","openai_key":"","logs":[],"runs":[],"notifications":[],"artifacts":[],"note_raw":"","note_md":"","note_plain":"","note_highlights":[],"skill_text":"","agents_text":"","prompt_text":"","sidebar":True,"muted":False,"active_run":None,"token_total":0,"run_count":0,"auth_user":"Guest","uploaded_text":"","last_error":""}
    for k,v in defaults.items():
        if k not in st.session_state: st.session_state[k]=v
def log_event(message, category="UI", severity="INFO", run_id=None):
    st.session_state.logs.append({"time":datetime.datetime.now().isoformat(timespec="seconds"),"category":category,"severity":severity,"message":str(message)[:1000],"run_id":run_id})
    st.session_state.logs=st.session_state.logs[-500:]
def notify(title,message,category="Task",severity="INFO"):
    st.session_state.notifications.insert(0,{"id":str(uuid.uuid4())[:8],"time":datetime.datetime.now().isoformat(timespec="seconds"),"title":title,"message":message,"category":category,"severity":severity,"read":False})
    st.session_state.notifications=st.session_state.notifications[:200]
def estimate_tokens(text): return max(1, (len(text or "")+3)//4)
def get_secret(provider):
    env_name={"Gemini":"GEMINI_API_KEY","OpenAI":"OPENAI_API_KEY"}.get(provider)
    if env_name and os.getenv(env_name): return os.getenv(env_name)
    return st.session_state.get({"Gemini":"gemini_key","OpenAI":"openai_key"}.get(provider,""),"")
def call_model(prompt, system="You are a helpful assistant.", temperature=0.2):
    provider=st.session_state.provider; model=st.session_state.model
    rid=str(uuid.uuid4())[:12]; started=time.time()
    st.session_state.active_run={"id":rid,"status":"Connecting","provider":provider,"model":model,"start":started}
    log_event(f"Run {rid}: connecting to {provider}/{model}","Inference","INFO",rid)
    try:
        if provider in ("Local OpenAI-compatible","Ollama"):
            base=st.session_state.local_url.strip().rstrip("/")
            if not re.match(r"^https?://",base): raise ValueError("Local endpoint must start with http:// or https://")
            headers={"Content-Type":"application/json"}
            if st.session_state.local_token: headers["Authorization"]="Bearer "+st.session_state.local_token
            import requests
            if provider=="Ollama" and "/api/chat" not in base:
                url=base if base.endswith("/api/chat") else base+"/api/chat"
                payload={"model":model,"stream":False,"messages":[{"role":"system","content":system},{"role":"user","content":prompt}]}
                r=requests.post(url,json=payload,headers=headers,timeout=120); r.raise_for_status(); data=r.json()
                answer=data.get("message",{}).get("content","")
                usage=data.get("prompt_eval_count",0)+data.get("eval_count",0)
            else:
                url=base if base.endswith("/chat/completions") else base+"/v1/chat/completions"
                payload={"model":model,"messages":[{"role":"system","content":system},{"role":"user","content":prompt}],"temperature":temperature}
                r=requests.post(url,json=payload,headers=headers,timeout=120); r.raise_for_status(); data=r.json()
                answer=data["choices"][0]["message"]["content"]; usage=(data.get("usage") or {}).get("total_tokens",0)
        elif provider=="OpenAI":
            key=get_secret("OpenAI")
            if not key: raise ValueError("OpenAI API key is required (or set OPENAI_API_KEY).")
            from openai import OpenAI
            response=OpenAI(api_key=key).chat.completions.create(model=model,messages=[{"role":"system","content":system},{"role":"user","content":prompt}],temperature=temperature)
            answer=response.choices[0].message.content or ""; usage=getattr(response.usage,"total_tokens",0) or 0
        elif provider=="Gemini":
            key=get_secret("Gemini")
            if not key: raise ValueError("Gemini API key is required (or set GEMINI_API_KEY).")
            import requests
            url=f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
            body={"systemInstruction":{"parts":[{"text":system}]},"contents":[{"parts":[{"text":prompt}]}],"generationConfig":{"temperature":temperature}}
            r=requests.post(url,json=body,timeout=120); r.raise_for_status(); data=r.json()
            answer="".join(p.get("text","") for p in data["candidates"][0]["content"]["parts"])
            usage=(data.get("usageMetadata") or {}).get("totalTokenCount",0)
        else: raise ValueError("Unsupported provider.")
        if not answer: raise ValueError("Provider returned an empty response.")
        exact=bool(usage); tokens=int(usage) if exact else estimate_tokens(prompt)+estimate_tokens(answer)
        run={"id":rid,"start":datetime.datetime.fromtimestamp(started).isoformat(timespec="seconds"),"duration":round(time.time()-started,2),"module":st.session_state.page,"provider":provider,"model":model,"status":"Completed","input_tokens":estimate_tokens(prompt),"output_tokens":estimate_tokens(answer),"total_tokens":tokens,"usage_kind":"exact" if exact else "estimated"}
        st.session_state.runs.insert(0,run); st.session_state.run_count+=1; st.session_state.token_total+=tokens
        st.session_state.active_run={**run,"status":"Completed"}; log_event(f"Run {rid} completed ({tokens} tokens, {run['usage_kind']})","Inference","SUCCESS",rid)
        notify("AI task completed",f"{provider}/{model} · {tokens} tokens")
        return answer
    except Exception as e:
        st.session_state.active_run={"id":rid,"status":"Error","error":str(e)}
        st.session_state.last_error=str(e); log_event(f"Run {rid} failed: {e}","Error","ERROR",rid); notify("AI task failed",str(e),"Error","ERROR")
        raise
def extract_upload(upload):
    name=upload.name.lower(); raw=upload.getvalue()
    if name.endswith((".txt",".md",".yaml",".yml",".json",".csv")): return raw.decode("utf-8",errors="replace")
    if name.endswith(".pdf"):
        try:
            from pypdf import PdfReader
            reader=PdfReader(io.BytesIO(raw)); text="\n\n".join(f"[Page {i+1}]\n{p.extract_text() or ''}" for i,p in enumerate(reader.pages))
            if len(text.strip())<40: st.warning("PDF 擷取文字偏少；可能是掃描影像，請檢查原文。")
            return text
        except Exception as e: raise ValueError(f"PDF extraction failed: {e}")
    raise ValueError("支援 TXT、Markdown、PDF、YAML、JSON、CSV。")
def init_db():
    with sqlite3.connect(DB_PATH) as c:
        c.execute("CREATE TABLE IF NOT EXISTS users(username TEXT PRIMARY KEY, salt BLOB NOT NULL, password_hash BLOB NOT NULL, display_name TEXT, created TEXT)")
def hash_password(password,salt): return hashlib.scrypt(password.encode(),salt=salt,n=2**14,r=8,p=1)
def safe_yaml(text):
    try:
        import yaml
        obj=yaml.safe_load(text)
        if not isinstance(obj,dict): raise ValueError("agents.yaml 頂層必須是 mapping/object。")
        return yaml.safe_dump(obj,allow_unicode=True,sort_keys=False), obj
    except ImportError: raise RuntimeError("請安裝 PyYAML：pip install pyyaml")
def apply_theme():
    dark=st.session_state.theme=="Dark"; bg="#101722" if dark else "#F4F7FB"; fg="#EDF2F7" if dark else "#172033"; surface="#1B2635" if dark else "#FFFFFF"; accent=PALETTES[st.session_state.palette]
    st.markdown(f"""<style>
    .stApp{{background:{bg};color:{fg}}} [data-testid="stSidebar"]{{background:{surface}}}
    .stButton>button{{border-radius:12px;border:1px solid {accent};}}
    .esub-card{{background:{surface};border:1px solid {accent}55;border-radius:16px;padding:1rem;margin:.35rem 0}}
    .esub-accent{{color:{accent};font-weight:700}} .small-muted{{opacity:.72;font-size:.85rem}}
    .run-pulse{{border-left:4px solid {accent};padding:.5rem 1rem;background:{surface};border-radius:8px}}
    </style>""",unsafe_allow_html=True)
def render_header():
    a,b,c=st.columns([3,2,2])
    with a: st.markdown(f"## ✦ {APP}"); st.caption("Local-first · Hybrid AI · Session-safe")
    with b:
        st.selectbox(tr("language"),["zh-TW","en","ja"],format_func=lambda x:{"zh-TW":"繁體中文","en":"English","ja":"日本語"}[x],key="locale")
        st.selectbox(tr("theme"),["Dark","Light"],key="theme")
    with c:
        st.selectbox(tr("palette"),list(PALETTES),key="palette")
        if st.button("🎰 Jackpot"): st.session_state.palette=random.choice(list(PALETTES)); st.rerun()
    st.divider()
def render_sidebar():
    with st.sidebar:
        st.markdown("### ✦ WOW Sidebar")
        st.caption(f"使用者：{st.session_state.auth_user} · {st.session_state.get('active_run',{}).get('status','Idle') if st.session_state.get('active_run') else 'Idle'}")
        st.metric("Session tokens · 估算／精確混合",st.session_state.token_total)
        st.progress(min(1,st.session_state.token_total/100000),text="Token budget indicator (100k reference)")
        st.markdown("**Quick links**")
        for key in ["home","notes","skills","pipeline","results","settings","logs"]:
            if st.button(tr(key),key="nav_"+key,use_container_width=True): st.session_state.page=key; st.rerun()
        st.markdown("**WOW AI quick launch**")
        if st.button("🧭 Quick Route Genius"): st.info("依任務：筆記整理→AI Note Keeper；YAML／技能→技能工作區；批次步驟→Pipeline。")
        if st.button("♻️ Session Recovery Oracle"): st.info(f"目前保留：筆記 {len(st.session_state.note_md)} 字元、{len(st.session_state.runs)} 次執行、{len(st.session_state.artifacts)} 個成果。")
        if st.button("💡 Insight Burst"): st.info("可嘗試摘要、行動項目擷取、術語解釋或改寫；請於筆記工作區選擇操作。")
        st.markdown("**Recent events**")
        for e in st.session_state.logs[-5:][::-1]: st.caption(f"{e['time'][11:]} · {e['severity']} · {e['message'][:70]}")
        st.caption(f"通知未讀：{sum(not n['read'] for n in st.session_state.notifications)}")
def provider_controls():
    st.subheader("模型路由 / Model Gateway")
    c1,c2=st.columns(2)
    with c1:
        st.selectbox(tr("provider"),["Local OpenAI-compatible","Ollama","Gemini","OpenAI"],key="provider")
        st.text_input("Model ID",key="model",help="不可用模型不會被靜默替換。")
    with c2:
        st.text_input(tr("local")+" (Base URL)",key="local_url")
        st.text_input("Local bearer token (session only)",type="password",key="local_token")
    if os.getenv("GEMINI_API_KEY"): st.success("Gemini key available from environment · hidden")
    elif st.session_state.provider=="Gemini": st.text_input("Gemini API key (session only)",type="password",key="gemini_key")
    if os.getenv("OPENAI_API_KEY"): st.success("OpenAI key available from environment · hidden")
    elif st.session_state.provider=="OpenAI": st.text_input("OpenAI API key (session only)",type="password",key="openai_key")
    st.caption("本機預設模型清單可手動輸入；Gemini 預設模型：gemini-3.1-flash-lite。")
    with st.expander("連線測試"):
        if st.button("測試目前設定"):
            try:
                answer=call_model("Reply with exactly: connection-ok","You are a connectivity test.")
                st.success("PASS · "+answer[:100])
            except Exception as e: st.error(f"FAIL · {e}")
def ai_magic_action(magic,text):
    prompts={
    "AI Keywords":"Extract 8-15 important keywords from this content as a comma-separated list:\n",
    "Smart Summarizer":"Provide short, medium, and detailed summaries with headings:\n",
    "Structure Refiner":"Reorganize into title, summary, topic headings, bullets, action items, open questions. Preserve facts and quotations:\n",
    "Action Extractor":"Extract action items, owner, deadline, and confidence. Mark unknowns as unknown:\n",
    "Terminology Explainer":"Identify specialized terms and explain them briefly in context:\n",
    "Rewrite Lens":"Rewrite this content as concise formal meeting notes. Preserve meaning; do not invent facts:\n"}
    return call_model(prompts[magic]+text)
def render_notes():
    st.header("📝 "+tr("notes"))
    up=st.file_uploader("上傳 TXT / Markdown / PDF",type=["txt","md","pdf"])
    if up:
        try:
            st.session_state.note_raw=extract_upload(up); log_event(f"Ingested {up.name}","File ingest","SUCCESS")
        except Exception as e: st.error(str(e))
    st.text_area("貼上或編輯原始內容",key="note_raw",height=180)
    c1,c2=st.columns(2)
    with c1:
        if st.button("✨ AI 整理成 Markdown",type="primary"):
            try: st.session_state.note_md=call_model("Organize into portable Markdown with title, summary, topic headings, bullets, action items if present, references if relevant. Do not invent facts:\n"+st.session_state.note_raw); st.session_state.note_plain=re.sub(r"[#*_>`]","",st.session_state.note_md)
            except Exception as e: st.error(str(e))
    with c2:
        if st.button("使用原文作為 Markdown"): st.session_state.note_md=st.session_state.note_raw
    st.subheader("AI Magics")
    magic=st.selectbox("選擇 Magic",MAGICS)
    if st.button("施展 AI Magic"):
        try:
            result=ai_magic_action(magic,st.session_state.note_md or st.session_state.note_raw)
            st.session_state.artifacts.insert(0,{"name":magic,"content":result,"time":datetime.datetime.now().isoformat(timespec="seconds")})
            st.session_state.note_md=result; st.success("已產生提案；原始輸入仍保留。")
        except Exception as e: st.error(str(e))
    mode=st.radio("編輯模式",["Markdown","Plain text","Preview"],horizontal=True)
    if mode=="Markdown": st.text_area("Markdown 編輯器",key="note_md",height=300)
    elif mode=="Plain text":
        st.text_area("純文字編輯器",key="note_plain",height=300)
        if st.button("將純文字套用至 Markdown"): st.session_state.note_md=st.session_state.note_plain
    else:
        content=st.session_state.note_md
        keywords=st.text_input("珊瑚色關鍵字（逗號分隔）")
        st.markdown(content)
        if keywords:
            for kw in [x.strip() for x in keywords.split(",") if x.strip()]:
                st.markdown(f'<span style="background:#FF7F7033;color:#FF7F70;padding:2px 5px;border-radius:4px">{kw}</span>',unsafe_allow_html=True)
    d1,d2,d3=st.columns(3)
    with d1: st.download_button("下載 Markdown",st.session_state.note_md or "","note.md","text/markdown")
    with d2: st.download_button("下載 TXT",st.session_state.note_plain or st.session_state.note_md or "","note.txt","text/plain")
    with d3:
        if st.button("複製內容（選取後 Ctrl+C）"): st.info("請在上方編輯器選取並複製；瀏覽器剪貼簿權限由使用者控制。")
def render_skills():
    st.header("🧩 Skill / Agent Workspace")
    tab1,tab2=st.tabs(["agents.yaml","SKILL.md"])
    with tab1:
        up=st.file_uploader("上傳 agents.yaml",type=["yaml","yml"],key="yaml_upload")
        if up: st.session_state.agents_text=up.getvalue().decode("utf-8",errors="replace")
        st.text_area("YAML 原文",key="agents_text",height=220)
        if st.button("安全解析／標準化 YAML"):
            try:
                normalized,obj=safe_yaml(st.session_state.agents_text); st.session_state.yaml_normalized=normalized; st.success(f"PASS · mapping with {len(obj)} top-level keys")
            except Exception as e: st.error(f"驗證失敗；原文保留：{e}")
        if st.session_state.get("yaml_normalized"):
            st.text_area("標準化預覽（確認後才套用）",st.session_state.yaml_normalized,height=180)
            if st.button("確認採用標準化內容"): st.session_state.agents_text=st.session_state.yaml_normalized; st.success("已套用")
            st.download_button("下載 normalized agents.yaml",st.session_state.yaml_normalized,"agents.yaml","text/yaml")
    with tab2:
        up2=st.file_uploader("上傳 SKILL.md",type=["md"],key="skill_upload")
        if up2: st.session_state.skill_text=up2.getvalue().decode("utf-8",errors="replace")
        st.text_area("Skill Markdown（支援 frontmatter 原文）",key="skill_text",height=350)
        st.download_button("下載 SKILL.md",st.session_state.skill_text,"SKILL.md","text/markdown")
def render_home():
    st.header("✦ "+tr("home"))
    cols=st.columns(4)
    metrics=[("執行次數",st.session_state.run_count),("Session tokens",st.session_state.token_total),("成果數",len(st.session_state.artifacts)),("通知未讀",sum(not n["read"] for n in st.session_state.notifications))]
    for col,(label,val) in zip(cols,metrics): col.metric(label,val)
    st.markdown("### Live Execution Pulse")
    run=st.session_state.active_run
    if run: st.markdown(f"<div class='run-pulse'><b>{run.get('status')}</b> · {run.get('provider','')} / {run.get('model','')} · {run.get('id','')}</div>",unsafe_allow_html=True)
    else: st.info("目前沒有執行中的模型任務。")
    st.markdown("### 10 WOW AI Features")
    st.dataframe([{"Feature":a,"Brief spec":b,"Comments":c} for a,b,c in WOW],use_container_width=True,hide_index=True)
    if st.session_state.runs: st.dataframe(st.session_state.runs[:20],use_container_width=True,hide_index=True)
def render_prompt():
    st.header("🪄 Template / Prompt Workspace")
    st.text_area("Prompt / Template",key="prompt_text",height=220)
    if st.button("執行提示詞"):
        try:
            out=call_model(st.session_state.prompt_text); st.session_state.artifacts.insert(0,{"name":"Prompt output","content":out,"time":datetime.datetime.now().isoformat(timespec="seconds")}); st.markdown(out)
        except Exception as e: st.error(str(e))
def render_pipeline():
    st.header("⚙️ Pipeline / Workflow Workspace")
    st.caption("以可追蹤步驟執行簡易文字工作流程；各步驟輸出均保留為 artifact。")
    source=st.text_area("Pipeline input",height=140)
    steps=st.multiselect("步驟",["整理摘要","擷取行動項目","正式改寫","術語解釋"],default=["整理摘要","擷取行動項目"])
    if st.button("執行 Pipeline",type="primary"):
        current=source
        for i,step in enumerate(steps,1):
            with st.status(f"Step {i}/{len(steps)} · {step}",expanded=True) as status:
                try:
                    current=call_model(f"{step}。請保留事實，不要捏造：\n{current}")
                    st.write(current[:1500]); status.update(label=f"Step {i} completed",state="complete")
                except Exception as e: status.update(label=f"Step {i} failed",state="error"); st.error(str(e)); break
        st.session_state.artifacts.insert(0,{"name":"Pipeline result","content":current,"time":datetime.datetime.now().isoformat(timespec="seconds")})
def render_results():
    st.header("📦 Results / Downloads")
    for i,a in enumerate(st.session_state.artifacts):
        with st.expander(f"{a['name']} · {a['time']}"):
            st.code(a["content"][:12000])
            st.download_button("下載成果",a["content"],f"artifact_{i}.md","text/markdown",key=f"artifact_dl_{i}")
def render_notifications():
    st.header("🔔 "+tr("notifications"))
    c1,c2=st.columns(2)
    with c1:
        if st.button("全部標示已讀"):
            for n in st.session_state.notifications: n["read"]=True
    with c2:
        st.toggle("暫時靜音提示",key="muted")
    for n in st.session_state.notifications:
        st.markdown(f"**{'●' if not n['read'] else '○'} {n['title']}** · {n['time']} · {n['severity']}  \n{n['message']}")
def render_account():
    st.header("👤 "+tr("account"))
    init_db()
    st.caption("Guest mode 可直接使用。帳戶資料使用 SQLite + scrypt salted password hash；本機部署請限制資料庫檔案權限。")
    tab1,tab2,tab3=st.tabs(["登入","註冊","個人資料"])
    with tab1:
        u=st.text_input("Username",key="login_u"); p=st.text_input("Password",type="password",key="login_p")
        if st.button("登入"):
            with sqlite3.connect(DB_PATH) as c: row=c.execute("SELECT salt,password_hash,display_name FROM users WHERE username=?",(u,)).fetchone()
            if row and hmac.compare_digest(hash_password(p,row[0]),row[1]): st.session_state.auth_user=u; st.success("登入成功")
            else: st.error("登入失敗；請檢查資料或使用註冊帳戶。")
    with tab2:
        u2=st.text_input("新帳號",key="reg_u"); d=st.text_input("顯示名稱",key="reg_d"); p1=st.text_input("新密碼",type="password",key="reg_p"); p2=st.text_input("確認密碼",type="password",key="reg_p2")
        if st.button("建立帳戶"):
            if len(p1)<12: st.error("密碼至少 12 字元。")
            elif p1!=p2: st.error("兩次密碼不一致。")
            elif not re.fullmatch(r"[A-Za-z0-9_.-]{3,64}",u2): st.error("帳號需為 3–64 個英數字、底線、點或連字號。")
            else:
                salt=secrets.token_bytes(16)
                try:
                    with sqlite3.connect(DB_PATH) as c: c.execute("INSERT INTO users VALUES(?,?,?,?,?)",(u2,salt,hash_password(p1,salt),d,datetime.datetime.now().isoformat()))
                    st.success("帳戶已建立。")
                except sqlite3.IntegrityError: st.error("帳號已存在。")
    with tab3:
        st.write("目前身份：",st.session_state.auth_user)
        if st.button("登出／切回訪客"): st.session_state.auth_user="Guest"; st.success("已切回訪客模式。")
        st.text_input("顯示名稱（工作階段）",key="display_name")
        st.caption("本版密碼重設採管理者／部署端流程；未設定郵件驗證時不提供不安全的自助重設。")
def render_settings():
    st.header("⚙️ "+tr("settings"))
    provider_controls()
    st.subheader("偏好與安全")
    st.checkbox("顯示 WOW Sidebar",key="sidebar")
    st.checkbox("允許雲端供應商（關閉可作為雲端出口開關）",key="cloud_enabled",value=st.session_state.get("cloud_enabled",True))
    st.caption("金鑰只保留在本次 Streamlit session；環境變數來源金鑰不顯示。勿將此開發伺服器直接暴露於不可信網路。")
    if st.button("執行啟動自我檢查"):
        checks={"Python runtime":True,"Session state":all(k in st.session_state for k in ["locale","provider","model","logs"]),"DB directory writable":os.access(str(DB_PATH.parent),os.W_OK),"Palette registry":len(PALETTES)==10,"Translations":all(x in I18N for x in ["zh-TW","en","ja"])}
        for k,v in checks.items(): st.write(("✅ PASS" if v else "❌ FAIL")+" · "+k)
def render_logs():
    st.header("🧪 "+tr("logs"))
    c1,c2=st.columns(2)
    with c1: search=st.text_input("搜尋紀錄")
    with c2: severity=st.selectbox("Severity",["ALL","INFO","SUCCESS","WARNING","ERROR"])
    rows=[x for x in st.session_state.logs if (severity=="ALL" or x["severity"]==severity) and search.lower() in x["message"].lower()]
    st.dataframe(rows[::-1],use_container_width=True,hide_index=True)
    st.download_button("匯出 logs.json",json.dumps(rows,ensure_ascii=False,indent=2),"logs.json","application/json")
    if st.session_state.last_error: st.error(st.session_state.last_error)
def main():
    st.set_page_config(page_title=APP,layout="wide",initial_sidebar_state="expanded")
    init_state(); apply_theme(); render_header()
    if st.session_state.sidebar: render_sidebar()
    pages={"home":render_home,"notes":render_notes,"prompt":render_prompt,"fill":render_prompt,"skills":render_skills,"pipeline":render_pipeline,"results":render_results,"notifications":render_notifications,"account":render_account,"settings":render_settings,"logs":render_logs}
    nav=st.selectbox("Workspace",list(pages),format_func=lambda k:tr(k),index=list(pages).index(st.session_state.page) if st.session_state.page in pages else 0,key="page_select")
    st.session_state.page=nav
    try: pages[nav]()
    except Exception as e:
        st.error(f"模組載入失敗，安全回退仍可使用其他功能：{e}")
        log_event(f"Render fallback: {e}","Error","ERROR")
    st.divider(); st.caption(f"Provider: {st.session_state.provider} · Model: {st.session_state.model} · State: {st.session_state.get('active_run',{}).get('status','Idle') if st.session_state.get('active_run') else 'Idle'}")
if __name__=="__main__": main()
