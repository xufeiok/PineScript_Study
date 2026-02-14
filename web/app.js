// 中文说明：Pine Script 学习系统前端主脚本
// 功能概述：
// - 加载课程数据（概念、代码对照、测验）
// - 交互逻辑：标签切换、测验反馈、进度存储、主题切换
// - 性能注意：数据体量小，使用原生 DOM 操作；持久化采用 localStorage，后端可选

(function () {
  // -------------------------------
  // 基础状态与工具函数
  // -------------------------------
  const state = {
    lessons: [],
    currentLessonIndex: null,
    currentQuizIndex: 0,
    answers: {},
    progress: loadProgress(),
  };

  // 加载进度（localStorage）
  function loadProgress() {
    try {
      const raw = localStorage.getItem("ps_progress");
      return raw ? JSON.parse(raw) : { lessons: {}, totalCompleted: 0 };
    } catch (e) {
      return { lessons: {}, totalCompleted: 0 };
    }
  }
  // 保存进度
  function saveProgress() {
    localStorage.setItem("ps_progress", JSON.stringify(state.progress));
  }

  // 文本复制
  async function copyText(text) {
    try {
      await navigator.clipboard.writeText(text);
    } catch (e) {
      // 兼容旧浏览器
      const ta = document.createElement("textarea");
      ta.value = text;
      document.body.appendChild(ta);
      ta.select();
      document.execCommand("copy");
      document.body.removeChild(ta);
    }
  }

  // 百分比格式化
  function pct(n) {
    const v = Math.max(0, Math.min(100, Math.round(n)));
    return `${v}%`;
  }

  // -------------------------------
  // 初始化：加载数据与事件绑定
  // -------------------------------
  document.addEventListener("DOMContentLoaded", async () => {
    bindGlobalEvents();
    await loadLessonsJSON();
    renderLessonList();
    // 默认选中第一个课程
    if (state.lessons.length > 0) {
      selectLesson(0);
    }
    updateGlobalProgress();
  });

  async function loadLessonsJSON() {
    // 中文说明：优先从本地文件加载，后端可替换相同路径
    try {
      // 添加时间戳防止缓存
      const res = await fetch("./data/lessons.json?t=" + Date.now());
      if (!res.ok) throw new Error("网络错误");
      const data = await res.json();
      state.lessons = data.lessons || [];
    } catch (e) {
      // 兜底：若加载失败，给出提示与空数据
      console.warn("课程数据加载失败，使用空数据。", e);
      state.lessons = [];
    }
  }

  function bindGlobalEvents() {
    // 中文说明：主题切换
    const toggleThemeBtn = document.getElementById("toggleThemeBtn");
    toggleThemeBtn.addEventListener("click", () => {
      document.body.classList.toggle("light");
    });

    // 进度重置
    document.getElementById("resetProgressBtn").addEventListener("click", () => {
      if (confirm("确定要重置所有学习进度吗？这将同时清除 VIP 解锁状态。")) {
        state.progress = { lessons: {}, totalCompleted: 0 };
        saveProgress();
        // 清除 VIP 状态
        localStorage.removeItem("ps_vip_user");
        
        renderLessonList();
        updateGlobalProgress();
        const idx = state.currentLessonIndex ?? 0;
        selectLesson(idx);
        alert("进度与权限已重置。");
      }
    });

    // Mobile Sidebar Logic
    const menuBtn = document.getElementById("menuBtn");
    const sidebar = document.querySelector(".sidebar");
    const overlay = document.getElementById("sidebarOverlay");

    if (menuBtn) {
      menuBtn.addEventListener("click", () => {
        sidebar.classList.toggle("active");
        overlay.classList.toggle("active");
      });
    }

    if (overlay) {
      overlay.addEventListener("click", () => {
        sidebar.classList.remove("active");
        overlay.classList.remove("active");
      });
    }

    // Mobile Modal Logic REMOVED
    /*
    const mobileBtn = document.getElementById("mobileBtn");
    const mobileModal = document.getElementById("mobileModal");
    ...
    */

    // 标签切换
    const tabs = document.querySelectorAll(".tab");
    tabs.forEach((t) => {
      t.addEventListener("click", () => {
        tabs.forEach((x) => x.classList.remove("active"));
        t.classList.add("active");
        const tab = t.dataset.tab;
        showPanel(tab);
      });
    });

    // 复制代码
    document.getElementById("copyPineBtn").addEventListener("click", () => {
      copyText(document.getElementById("pineCode").textContent);
    });
    document.getElementById("copyPyBtn").addEventListener("click", () => {
      copyText(document.getElementById("pythonCode").textContent);
    });

    // 测验按钮
    document.getElementById("submitQuizBtn").addEventListener("click", handleSubmitQuiz);
    document.getElementById("nextQuizBtn").addEventListener("click", () => {
      state.currentQuizIndex++;
      renderQuiz();
    });
  }

  function showPanel(name) {
    const panels = {
      concept: document.getElementById("panelConcept"),
      code: document.getElementById("panelCode"),
      quiz: document.getElementById("panelQuiz"),
    };
    Object.values(panels).forEach((p) => p.classList.add("hidden"));
    (panels[name] || panels.concept).classList.remove("hidden");
  }

  // -------------------------------
  // 渲染：课程列表与选中
  // -------------------------------
  function renderLessonList() {
    const ul = document.getElementById("lessonList");
    ul.innerHTML = "";
    
    let lastCategory = null;

    state.lessons.forEach((lsn, i) => {
      // Add category header if needed
      if (lsn.category && lsn.category !== lastCategory) {
        const catLi = document.createElement("li");
        catLi.className = "category-header";
        catLi.innerText = lsn.category;
        ul.appendChild(catLi);
        lastCategory = lsn.category;
      }

      const li = document.createElement("li");
      li.className = i === state.currentLessonIndex ? "active lesson-item" : "lesson-item";
      li.innerHTML = `
        <span class="lesson-title">${lsn.title}</span>
        <span class="lesson-status">${progressMark(i)}</span>
      `;
      li.addEventListener("click", () => selectLesson(i));
      ul.appendChild(li);
    });
  }

  function progressMark(i) {
    const lsn = state.lessons[i];
    const prog = state.progress.lessons[lsn.id];
    if (!prog) return "未开始";
    if (prog.quizDone && prog.readDone && prog.codeDone) return "已完成";
    const done = ["readDone", "codeDone", "quizDone"].filter((k) => prog[k]).length;
    return `${done}/3`;
  }

  function selectLesson(index) {
    state.currentLessonIndex = index;
    state.currentQuizIndex = 0;
    renderLessonList();
    const lsn = state.lessons[index];
    document.getElementById("lessonTitle").innerText = lsn.title;
    document.getElementById("lessonSubtitle").innerText = lsn.subtitle || "";

    // Content Locking Logic
    const contentArea = document.querySelector(".content-area");
    // Remove existing lock overlay if any
    const existingOverlay = document.getElementById("lockOverlay");
    if (existingOverlay) existingOverlay.remove();

    const paidCategoryKeywords = ["内置指标", "量化策略"];
    const isPaidContent = paidCategoryKeywords.some((c) => lsn.category && lsn.category.includes(c));
    
    // User is VIP if they have paid (stored in localStorage)
    // -------------------------------
    // 用户白名单配置
    // -------------------------------
    // 自动检测本地开发环境（localhost），如果是管理员/开发者则免扫码直接解锁
    // 将此变量设为 true，即可在本地环境中自动获得 VIP 权限
    const isLocalDev = ["localhost", "127.0.0.1"].includes(location.hostname);
    // [已禁用自动解锁] 为了演示扫码逻辑，此处注释掉自动解锁代码
    /* 
    if (isLocalDev && !localStorage.getItem("ps_vip_user")) {
        // 自动写入白名单标记
        console.log("检测到本地开发环境，自动激活管理员白名单权限。");
        localStorage.setItem("ps_vip_user", "admin_whitelist_auto");
    }
    */

    const isVip = !!localStorage.getItem("ps_vip_user");

    if ((lsn.isLocked || isPaidContent) && !isVip) {
      renderLockedOverlay(lsn, contentArea);
      return; // Stop rendering content
    }

    renderConcept(lsn);
    renderCode(lsn);
    renderQuiz();
    updateGlobalProgress();
    // 默认显示概念面板
    document.querySelectorAll(".tab").forEach((x) => x.classList.remove("active"));
    document.querySelector('.tab[data-tab="concept"]').classList.add("active");
    showPanel("concept");
  }

  function renderLockedOverlay(lsn, container) {
    // Clear existing content
    document.getElementById("conceptBody").innerHTML = "";
    document.getElementById("conceptSummary").innerHTML = "";
    document.getElementById("pineCode").textContent = "";
    document.getElementById("pythonCode").textContent = "";
    document.getElementById("quizBody").innerHTML = "";

    const overlay = document.createElement("div");
    overlay.id = "lockOverlay";
    overlay.className = "lock-overlay";
    overlay.innerHTML = `
      <div class="lock-content">
        <div class="lock-icon">🔒</div>
        <h3>VIP 专属课程</h3>
        <p>本课程属于 "${lsn.category}"，为付费内容。</p>
        <p>一次性支付 <strong>¥9.0</strong> 即可永久解锁所有高级课程。</p>
        
        <div class="pay-methods">
          <div class="pay-item">
            <img src="./assets/wechat_pay.png" class="qr-img" alt="微信支付" onerror="this.style.display='none';this.parentElement.innerHTML+='<div class=\'qr-placeholder\' style=\'background:#2fac66\'>微信支付</div>'">
            <span>微信扫码</span>
          </div>
          <div class="pay-item">
            <img src="./assets/alipay.png" class="qr-img" alt="支付宝" onerror="this.style.display='none';this.parentElement.innerHTML+='<div class=\'qr-placeholder\' style=\'background:#1677ff\'>支付宝</div>'">
            <span>支付宝扫码</span>
          </div>
        </div>

        <div class="verify-section">
          <p class="instruction">
            <strong>获取方式：</strong>扫码支付时请备注您的<span style="color:#e67e22">邮箱或微信号</span>。<br>
            管理员核对后将通过备注的联系方式发送<strong>激活码</strong>。
          </p>
          <div class="code-input-group" style="margin: 15px 0; display: flex; gap: 8px; justify-content: center;">
            <input type="text" id="activationCodeInput" placeholder="请输入激活码" style="padding: 8px; border: 1px solid #ddd; border-radius: 4px; width: 200px;">
            <button id="unlockBtn" class="btn-primary" style="white-space: nowrap;">验证并解锁</button>
          </div>
          <p id="unlockMsg" style="font-size: 12px; height: 16px;"></p>
        </div>
      </div>
    `;
    container.appendChild(overlay);

    // Verify Logic - Manual Code
    document.getElementById("unlockBtn").addEventListener("click", () => {
       const inputEl = document.getElementById("activationCodeInput");
       const msgEl = document.getElementById("unlockMsg");
       const btn = document.getElementById("unlockBtn");
       
       const userCode = inputEl.value.trim();
       
       if (!userCode) {
         msgEl.style.color = "red";
         msgEl.innerText = "请输入激活码";
         return;
       }

       btn.disabled = true;
       btn.innerText = "验证中...";

       // 简单的本地验证逻辑 (方案 A)
       // 预设密码: pinegood888 (不区分大小写)
       const validCodes = ["PINEGOOD888"];
       
       setTimeout(() => {
         if (validCodes.includes(userCode.toUpperCase())) {
            // Success
            localStorage.setItem("ps_vip_user", "manual_code_" + userCode);
            msgEl.style.color = "green";
            msgEl.innerText = "验证成功！正在解锁...";
            
            setTimeout(() => {
                alert("恭喜！已成功解锁所有 VIP 课程。");
                selectLesson(state.currentLessonIndex); // Re-render
            }, 500);
         } else {
            // Fail
            msgEl.style.color = "red";
            msgEl.innerText = "激活码无效，请检查或联系管理员。";
            btn.disabled = false;
            btn.innerText = "验证并解锁";
         }
       }, 600); // Slight delay for UX
    });
  }

  // -------------------------------
  // 简单解密工具 (XOR)
  // -------------------------------
  function xorDecrypt(encryptedBase64, key) {
    if (!encryptedBase64) return "";
    try {
      const encryptedBytes = Uint8Array.from(atob(encryptedBase64), c => c.charCodeAt(0));
      const keyBytes = new TextEncoder().encode(key);
      const decryptedBytes = new Uint8Array(encryptedBytes.length);
      
      for (let i = 0; i < encryptedBytes.length; i++) {
        decryptedBytes[i] = encryptedBytes[i] ^ keyBytes[i % keyBytes.length];
      }
      return new TextDecoder().decode(decryptedBytes);
    } catch (e) {
      console.error("Decryption failed:", e);
      return "[内容解析错误]";
    }
  }

  // -------------------------------
  // 概念讲解与总结
  // -------------------------------
  function renderConcept(lsn) {
    const body = document.getElementById("conceptBody");
    body.classList.toggle("is-reference", !!(lsn.category && lsn.category.includes("参考资料")));
    
    // Decrypt content if needed
    let main = lsn.concept || "";
    let extra = lsn.concept_extra || "";
    
    if (lsn.isEncrypted) {
        // Retrieve key from storage (stored as 'manual_code_PINEGOOD888')
        const stored = localStorage.getItem("ps_vip_user") || "";
        const userKey = stored.replace("manual_code_", "").trim();
        
        if (main.startsWith("ENC:")) main = xorDecrypt(main.substring(4), userKey);
        if (extra.startsWith("ENC:")) extra = xorDecrypt(extra.substring(4), userKey);
    }
    
    body.innerHTML = main || extra ? `${main}${extra}` : "暂无内容";
    const sum = document.getElementById("conceptSummary");
    sum.innerHTML = "";
    (lsn.summary || []).forEach((s) => {
      const li = document.createElement("li");
      li.textContent = s;
      sum.appendChild(li);
    });
    markLessonProgress(lsn.id, "readDone", true);
  }

  // -------------------------------
  // 代码对照（Pine Script vs Python）
  // -------------------------------
  function renderCode(lsn) {
    const pineEl = document.getElementById("pineCode");
    const pyEl = document.getElementById("pythonCode");
    
    let pCode = lsn.pine_code || "";
    let pyCode = lsn.python_code || "";
    
    if (lsn.isEncrypted) {
        const stored = localStorage.getItem("ps_vip_user") || "";
        const userKey = stored.replace("manual_code_", "").trim();
        
        if (pCode.startsWith("ENC:")) pCode = xorDecrypt(pCode.substring(4), userKey);
        if (pyCode.startsWith("ENC:")) pyCode = xorDecrypt(pyCode.substring(4), userKey);
    }
    
    // 调试：打印一下看看内容
    // console.log("Rendering Pine Code:", pCode);
    
    // 尝试方案 A: 纯文本注入，依赖 CSS pre-wrap
    pineEl.textContent = pCode;
    pyEl.textContent = pyCode;
    
    // 重置 class
    pineEl.className = "language-javascript";
    pyEl.className = "language-python";
    pineEl.removeAttribute("data-highlighted");
    pyEl.removeAttribute("data-highlighted");

    // 只有当 hljs 存在且加载成功时才高亮
    if (window.hljs) {
      hljs.highlightElement(pineEl);
      hljs.highlightElement(pyEl);
    } else {
      console.warn("Highlight.js not loaded");
    }

    markLessonProgress(lsn.id, "codeDone", true);
  }

  // -------------------------------
  // 测验：主动回忆 + 即时反馈 + 简单间隔重复策略
  // -------------------------------
  function renderQuiz() {
    const lsn = state.lessons[state.currentLessonIndex];
    const quiz = lsn.quiz || [];
    const idx = state.currentQuizIndex;
    const title = document.getElementById("quizTitle");
    const prog = document.getElementById("quizProgress");
    const body = document.getElementById("quizBody");
    const feedback = document.getElementById("quizFeedback");
    const submitBtn = document.getElementById("submitQuizBtn");
    const nextBtn = document.getElementById("nextQuizBtn");

    feedback.innerHTML = "";
    nextBtn.disabled = true;
    submitBtn.disabled = false;

    if (quiz.length === 0) {
      title.innerText = "本课暂无测验";
      prog.innerText = "0 / 0";
      body.innerHTML = "";
      submitBtn.disabled = true;
      markLessonProgress(lsn.id, "quizDone", true);
      return;
    }

    if (idx >= quiz.length) {
      title.innerText = "测验完成";
      prog.innerText = `${quiz.length} / ${quiz.length}`;
      body.innerHTML = "";
      submitBtn.disabled = true;
      nextBtn.disabled = true;
      feedback.innerHTML = `<span class="ok">恭喜，本课测验已完成！</span>`;
      markLessonProgress(lsn.id, "quizDone", true);
      return;
    }

    const q = quiz[idx];
    title.innerText = q.q;
    prog.innerText = `${idx + 1} / ${quiz.length}`;
    body.innerHTML = q.choices
      .map(
        (c, i) => `
      <label class="choice" data-idx="${i}">
        <input type="radio" name="choice" value="${i}" />
        <span>${c.text}</span>
      </label>
    `
      )
      .join("");
  }

  function handleSubmitQuiz() {
    const lsn = state.lessons[state.currentLessonIndex];
    const quiz = lsn.quiz || [];
    const idx = state.currentQuizIndex;
    if (idx >= quiz.length) return;
    const q = quiz[idx];
    const selected = document.querySelector('input[name="choice"]:checked');
    const feedback = document.getElementById("quizFeedback");
    const nextBtn = document.getElementById("nextQuizBtn");
    const submitBtn = document.getElementById("submitQuizBtn");
    const body = document.getElementById("quizBody");

    if (!selected) {
      feedback.innerHTML = `<span class="bad">请先选择一个选项</span>`;
      return;
    }
    const choiceIdx = Number(selected.value);
    const correct = !!q.choices[choiceIdx]?.isCorrect;

    // 展示对错并给予讲解
    body.querySelectorAll(".choice").forEach((el, i) => {
      el.classList.toggle("correct", !!q.choices[i]?.isCorrect);
      if (i === choiceIdx && !q.choices[i]?.isCorrect) el.classList.add("wrong");
    });
    feedback.innerHTML = correct
      ? `<span class="ok">回答正确！</span> ${q.explain || ""}`
      : `<span class="bad">回答错误。</span> ${q.explain || ""}`;

    // 简单的间隔重复：错误题标记复习
    const key = `${lsn.id}:${idx}`;
    state.answers[key] = { correct, ts: Date.now() };

    nextBtn.disabled = false;
    submitBtn.disabled = true;
  }

  // -------------------------------
  // 进度：课程维度 + 全局百分比
  // -------------------------------
  function markLessonProgress(lessonId, field, val) {
    if (!state.progress.lessons[lessonId]) {
      state.progress.lessons[lessonId] = { readDone: false, codeDone: false, quizDone: false };
    }
    state.progress.lessons[lessonId][field] = val;
    saveProgress();
    updateGlobalProgress();
  }

  function updateGlobalProgress() {
    const ids = state.lessons.map((l) => l.id);
    let done = 0;
    ids.forEach((id) => {
      const p = state.progress.lessons[id];
      if (p && p.readDone && p.codeDone && p.quizDone) done++;
    });
    const total = Math.max(1, ids.length);
    const percent = (done / total) * 100;
    document.getElementById("progressFill").style.width = pct(percent);
    document.getElementById("progressText").innerText = `${pct(percent)} 完成`;
  }
})();
