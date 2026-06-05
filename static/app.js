const form = document.querySelector("#profileForm");
const submitBtn = document.querySelector("#submitBtn");
const sampleBtn = document.querySelector("#sampleBtn");
const languageBtn = document.querySelector("#languageBtn");
const statusDot = document.querySelector("#statusDot");
const statusTitle = document.querySelector("#statusTitle");
const statusText = document.querySelector("#statusText");
const emptyState = document.querySelector("#emptyState");
const resultContent = document.querySelector("#resultContent");
const categoryTitle = document.querySelector("#categoryTitle");
const confidenceValue = document.querySelector("#confidenceValue");
const cards = document.querySelector("#cards");
const models = document.querySelector("#models");

let currentLanguage = localStorage.getItem("sanad-language") || "ar";
let lastResult = null;

const translations = {
  ar: {
    navStart: "ابدأ التحليل",
    navResult: "النتيجة",
    heroTitle: "خلّ الذكاء الاصطناعي يساعدك تختار استثمارك الأنسب",
    heroLead: "أدخل بياناتك، والنظام يقارن بين الودائع، الصناديق السعودية، الأسهم السعودية، الأسهم الأمريكية، والمحفظة المختلطة.",
    heroAction: "ابدأ الآن",
    statusTrainingTitle: "جاري تجهيز النماذج",
    statusTrainingText: "يتم تدريب نماذج الذكاء الاصطناعي مرة واحدة عند تشغيل الموقع.",
    statusReadyTitle: "النماذج جاهزة",
    statusReadyText: "يمكنك الآن إرسال بياناتك والحصول على توصية مباشرة.",
    statusErrorTitle: "تعذر تجهيز النماذج",
    statusWaitingText: "قد يستغرق التدريب الأولي بعض الوقت حسب الجهاز.",
    formTitle: "بياناتك",
    sample: "تعبئة مثال",
    age: "العمر",
    monthlyIncome: "الدخل الشهري بالريال",
    capital: "رأس المال الاستثماري",
    duration: "مدة الاستثمار",
    durationShort: "قريب، أحتاج المبلغ بسرعة",
    durationMedium: "فترة متوسطة",
    durationLong: "فترة طويلة، ما أحتاجه قريب",
    risk: "تحمل المخاطر",
    low: "منخفض",
    medium: "متوسط",
    high: "مرتفع",
    goal: "الهدف الاستثماري",
    income: "دخل ثابت",
    balanced: "توازن",
    growth: "نمو رأس المال",
    experience: "مستوى الخبرة",
    beginner: "مبتدئ",
    intermediate: "متوسط",
    advanced: "متقدم",
    liquidity: "الحاجة للسيولة",
    liquidityHigh: "مرتفعة",
    liquidityMedium: "متوسطة",
    liquidityLow: "منخفضة",
    submit: "اعرض التوصية",
    analyzing: "جاري التحليل...",
    emptyTitle: "النتيجة بتطلع هنا",
    emptyText: "بعد ما تكتمل النماذج، أرسل بياناتك وراح تظهر لك التوصية وقائمة الخيارات المناسبة.",
    recommendedArea: "المجال المقترح",
    confidence: "ثقة النموذج",
    noRecommendations: "لا توجد توصيات تفصيلية مطابقة",
    recommendation: "توصية",
    open: "فتح",
    link: "رابط",
    modelTitle: "أفضل النماذج المستخدمة",
    errorTitle: "حدث خطأ",
    defaultError: "تعذر توليد التوصية",
    fillAll: "الرجاء تعبئة جميع الحقول المطلوبة.",
    languageButton: "English",
  },
  en: {
    navStart: "Start analysis",
    navResult: "Result",
    heroTitle: "Let AI help you choose the best investment path",
    heroLead: "Enter your profile, and the system compares deposits, Saudi funds, Saudi stocks, US stocks, and a mixed portfolio.",
    heroAction: "Get started",
    statusTrainingTitle: "Preparing models",
    statusTrainingText: "The AI models train once when the website starts.",
    statusReadyTitle: "Models are ready",
    statusReadyText: "You can now submit your information and receive a recommendation.",
    statusErrorTitle: "Could not prepare models",
    statusWaitingText: "Initial training may take a little time depending on the device.",
    formTitle: "Your profile",
    sample: "Fill sample",
    age: "Age",
    monthlyIncome: "Monthly income in SAR",
    capital: "Investment capital",
    duration: "Investment duration",
    durationShort: "Soon, I may need the money quickly",
    durationMedium: "Medium period",
    durationLong: "Long period, I do not need it soon",
    risk: "Risk tolerance",
    low: "Low",
    medium: "Medium",
    high: "High",
    goal: "Investment goal",
    income: "Steady income",
    balanced: "Balanced",
    growth: "Capital growth",
    experience: "Experience level",
    beginner: "Beginner",
    intermediate: "Intermediate",
    advanced: "Advanced",
    liquidity: "Liquidity need",
    liquidityHigh: "High",
    liquidityMedium: "Medium",
    liquidityLow: "Low",
    submit: "Show recommendation",
    analyzing: "Analyzing...",
    emptyTitle: "Your result will appear here",
    emptyText: "Once the models are ready, submit your information to see the recommendation and matching options.",
    recommendedArea: "Recommended area",
    confidence: "Model confidence",
    noRecommendations: "No matching detailed recommendations",
    recommendation: "Recommendation",
    open: "Open",
    link: "Link",
    modelTitle: "Best models used",
    errorTitle: "Something went wrong",
    defaultError: "Could not generate the recommendation",
    fillAll: "Please fill in all required fields.",
    languageButton: "العربية",
  },
};

const categoryLabels = {
  ar: {
    Deposits: "الودائع والمنتجات الادخارية",
    Saudi_Funds: "الصناديق الاستثمارية السعودية",
    Saudi_Stocks: "سوق الأسهم السعودي",
    US_Stocks: "سوق الأسهم الأمريكي",
    Mixed: "محفظة مختلطة",
  },
  en: {
    Deposits: "Deposits and savings products",
    Saudi_Funds: "Saudi investment funds",
    Saudi_Stocks: "Saudi stock market",
    US_Stocks: "US stock market",
    Mixed: "Mixed portfolio",
  },
};

const fieldLabels = {
  ar: {
    Category: "الفئة",
    bank: "البنك",
    product_name: "المنتج",
    product_type: "نوع المنتج",
    min_amount_sar: "الحد الأدنى",
    max_amount_sar: "الحد الأعلى",
    tenor_months: "المدة بالأشهر",
    liquidity_level: "السيولة",
    annual_return_pct: "العائد السنوي",
    rate_type: "نوع العائد",
    deposit_match_score: "درجة الملاءمة",
    Date: "آخر تاريخ",
    Ticker: "الرمز",
    Company_Name: "الاسم",
    AI_Prediction: "توقع النموذج",
    AI_Confidence: "ثقة الأصل",
    Close: "الإغلاق",
    Volume: "الحجم",
    source_url: "المصدر",
  },
  en: {
    Category: "Category",
    bank: "Bank",
    product_name: "Product",
    product_type: "Product type",
    min_amount_sar: "Minimum amount",
    max_amount_sar: "Maximum amount",
    tenor_months: "Term in months",
    liquidity_level: "Liquidity",
    annual_return_pct: "Annual return",
    rate_type: "Rate type",
    deposit_match_score: "Match score",
    Date: "Latest date",
    Ticker: "Ticker",
    Company_Name: "Name",
    AI_Prediction: "AI prediction",
    AI_Confidence: "Asset confidence",
    Close: "Close",
    Volume: "Volume",
    source_url: "Source",
  },
};

function t(key) {
  return translations[currentLanguage][key] || translations.ar[key] || key;
}

function applyLanguage(language) {
  currentLanguage = language;
  localStorage.setItem("sanad-language", language);
  document.documentElement.lang = language;
  document.documentElement.dir = language === "ar" ? "rtl" : "ltr";
  document.body.classList.toggle("is-english", language === "en");

  document.querySelectorAll("[data-i18n]").forEach((element) => {
    element.textContent = t(element.dataset.i18n);
  });
  languageBtn.textContent = t("languageButton");

  if (lastResult) {
    renderResult(lastResult);
  }
}

function formatValue(key, value) {
  if (value === null || value === undefined || value === "") return "-";
  if (key.includes("Confidence") || key.includes("score")) {
    const num = Number(value);
    return Number.isFinite(num) ? `${Math.round(num * 100)}%` : value;
  }
  if (typeof value === "number") {
    return new Intl.NumberFormat(currentLanguage === "ar" ? "ar-SA" : "en-US", {
      maximumFractionDigits: 2,
    }).format(value);
  }
  if (key === "source_url") {
    return t("link");
  }
  return String(value);
}

function getTitle(record, index) {
  return (
    record.product_name ||
    record.Company_Name ||
    record.Ticker ||
    record.bank ||
    `${t("recommendation")} ${index + 1}`
  );
}

function renderCards(records) {
  cards.innerHTML = "";
  if (!records.length) {
    cards.innerHTML = `<div class="card"><h3>${t("noRecommendations")}</h3></div>`;
    return;
  }

  records.forEach((record, index) => {
    const card = document.createElement("article");
    card.className = "card";
    const title = document.createElement("h3");
    title.textContent = getTitle(record, index);
    card.appendChild(title);

    Object.entries(record)
      .filter(([key]) => key !== "product_name" && key !== "Company_Name")
      .slice(0, 8)
      .forEach(([key, value]) => {
        const row = document.createElement("div");
        row.className = "metric";
        const label = document.createElement("span");
        label.textContent = fieldLabels[currentLanguage][key] || key;
        const strong = document.createElement("strong");
        if (key === "source_url" && value) {
          const link = document.createElement("a");
          link.href = value;
          link.target = "_blank";
          link.rel = "noreferrer";
          link.textContent = t("open");
          strong.appendChild(link);
        } else {
          strong.textContent = formatValue(key, value);
        }
        row.append(label, strong);
        card.appendChild(row);
      });

    cards.appendChild(card);
  });
}

function renderResult(result) {
  categoryTitle.textContent =
    categoryLabels[currentLanguage][result.recommended_category] ||
    result.recommended_category_ar ||
    result.recommended_category;
  confidenceValue.textContent = formatValue("category_confidence", result.category_confidence);
  renderCards(result.final_recommendations);
}

async function refreshStatus() {
  const response = await fetch("/api/status");
  const status = await response.json();

  statusDot.className = "status-dot";
  if (status.ready) {
    statusDot.classList.add("ready");
    statusTitle.textContent = t("statusReadyTitle");
    statusText.textContent = t("statusReadyText");
    submitBtn.disabled = false;
    clearInterval(statusTimer);
    loadModels();
  } else if (status.error) {
    statusDot.classList.add("error");
    statusTitle.textContent = t("statusErrorTitle");
    statusText.textContent = status.error;
  } else {
    statusTitle.textContent = t("statusTrainingTitle");
    statusText.textContent = t("statusWaitingText");
  }
}

async function loadModels() {
  const response = await fetch("/api/models");
  const payload = await response.json();
  if (!payload.ready) return;

  models.innerHTML = `
    <strong>${t("modelTitle")}</strong>
    <ul>
      ${payload.models
        .map(
          (model) => `
            <li>
              ${model.scope}<br />
              <strong>${model.best_model}</strong> - F1 ${formatValue("score", model.f1_score)}
            </li>
          `,
        )
        .join("")}
    </ul>
  `;
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  submitBtn.disabled = true;
  submitBtn.textContent = t("analyzing");

  const payload = Object.fromEntries(new FormData(form).entries());
  payload.preferred_market = "Both";
  try {
    const response = await fetch("/api/recommend", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.message || t("defaultError"));

    lastResult = result;
    emptyState.classList.add("hidden");
    resultContent.classList.remove("hidden");
    renderResult(result);
  } catch (error) {
    emptyState.classList.remove("hidden");
    resultContent.classList.add("hidden");
    emptyState.innerHTML = `<span>!</span><h2>${t("errorTitle")}</h2><p>${error.message}</p>`;
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = t("submit");
  }
});

sampleBtn.addEventListener("click", () => {
  const sample = {
    age: 53,
    monthly_income: 20000,
    investment_capital: 700000,
    investment_horizon: "short",
    risk_tolerance: "low",
    investment_goal: "income",
    experience_level: "intermediate",
    liquidity_need: "high",
  };
  Object.entries(sample).forEach(([key, value]) => {
    if (form.elements[key]) {
      form.elements[key].value = value;
    }
  });
});

languageBtn.addEventListener("click", () => {
  applyLanguage(currentLanguage === "ar" ? "en" : "ar");
  refreshStatus();
  loadModels();
});

applyLanguage(currentLanguage);
const statusTimer = setInterval(refreshStatus, 2500);
refreshStatus();
