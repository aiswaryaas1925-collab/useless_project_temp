import { useState } from "react";
import "./App.css";
import redditImage from "./assets/redditmaman.png";
function App() {
 const [page, setPage] = useState("dashboard");
 const [ignored, setIgnored] = useState("");
 const [problem, setProblem] = useState("");
 const [language, setLanguage] = useState("en");
 const text = {
  en: {
    meet: "MEET YOUR ADVISORS",
    subtitle: "Three experts. Zero qualifications. Unlimited bad advice.",
    ready: "READY TO RUIN YOUR PROBLEM?",
    start: "🔥 GET THE WORST ADVICE",
  },
  ml: {
    meet: "നിങ്ങളുടെ ഉപദേശകരെ പരിചയപ്പെടൂ",
    subtitle: "മൂന്ന് വിദഗ്ധർ. യോഗ്യത പൂജ്യം. മോശം ഉപദേശം അനന്തം.",
    ready: "നിങ്ങളുടെ പ്രശ്നം നശിപ്പിക്കാൻ തയ്യാറാണോ?",
    start: "🔥 ഏറ്റവും മോശം ഉപദേശം നേടൂ",
  },
};

  return (
    <div className="app">

      {/* NAVBAR */}
      <nav className="navbar">

        <div className="logo">
          <span className="skull">☠</span>
          <div>
            <div className="logo-title">
              <span>WORST</span> ADVICE
            </div>
            <small>COMMITTEE</small>
          </div>
        </div>

        <div className="nav-links">
          <button
            className={page === "dashboard" ? "active" : ""}
            onClick={() => setPage("dashboard")}
          >
            ⌂ Home
          </button>

          <button onClick={() => setPage("shame")}>
  ☠ Hall of Shame
</button>
          <button>⚙ Why this exists?</button>
          <button>ⓘ About</button>
        </div>

        <div className="nav-right">
          <button>🔊</button>
         <button onClick={() => setLanguage(language === "en" ? "ml" : "en")}>
  {language === "en" ? "മലയാളം" : "English"}
</button>
        </div>

      </nav>


      {/* DASHBOARD */}
      {page === "dashboard" && (
        <main className="dashboard">

          <div className="welcome-tag">
            ☠ WELCOME TO THE COMMITTEE
          </div>

          <h1>
  {language === "ml" ? (
    <span>{text.ml.meet}</span>
  ) : (
    <>MEET YOUR <span>ADVISORS</span></>
  )}
</h1>
          <p className="subtitle">
            Three experts. Zero qualifications. Unlimited bad advice.
          </p>


          {/* CHARACTER CARDS */}
          <div className="characters">

            <div className="character-card chechi">
              <img
  className="character-image"
  src="/src/assets/chechi.png"
  alt="Chechi"
/>

              <div className="character-heading">
  <h2>CHECHI</h2>
  <span>— THE EMOTIONAL EXPERT</span>
</div>

              <p className="quote">
                "Don't worry. I have a solution."
              </p>

              <div className="badness">
                ☠ BADNESS: <strong>86%</strong>
              </div>
            </div>


            <div className="character-card upadeshi">
              <img
  className="character-image"
  src="/src/assets/nattile updeshi.png"
  alt="Nattile Upadeshi"
/>

              <div className="character-heading">
  <h2>NATTILE UPADESHI</h2>
  <span>— THE UNSOLICITED EXPERT</span>
</div>

              <p className="quote">
                "In my time, we had a solution for everything."
              </p>

              <div className="badness">
                ☠ BADNESS: <strong>94%</strong>
              </div>
            </div>


            <div className="character-card reddit">
              <img
  className="character-image"
  src={redditImage}
  alt="Reddit Maman"
/>

              <div className="character-heading">
  <h2>REDDIT MAMAN</h2>
  <span>— THE INTERNET EXPERT</span>
</div>
              <p className="quote">
                "Bro, I saw this on Reddit."
              </p>

              <div className="badness">
                ☠ BADNESS: <strong>99%</strong>
              </div>
            </div>

          </div>


          {/* START BUTTON */}
          <div className="start-section">

            <p>READY TO RUIN YOUR PROBLEM?</p>

            <button
              className="start-btn"
              onClick={() => setPage("chat")}
            >
              🔥 GET THE WORST ADVICE
            </button>

          </div>

        </main>
      )}


      {/* CHAT PAGE */}
{page === "chat" && (
  <main className="chat-page">

    <div className="welcome-tag">
      ☠ WORST ADVICE SESSION
    </div>

    <h1>
      WHAT'S <span>YOUR PROBLEM?</span>
    </h1>

    <p className="subtitle">
      Tell the committee what's going wrong.
      <br />
      They promise absolutely nothing.
    </p>

    <div className="problem-box">

      <div className="input-label">
        🧠 YOUR PROBLEM
      </div>

      <textarea
  className="problem-input"
  placeholder="Tell us your problem... exam tomorrow, relationship drama, career confusion..."
  value={problem}
  onChange={(e) => setProblem(e.target.value)}
  maxLength={500}
/>

            <div className="input-footer">
        <span>⚠ Your problem will be made significantly worse.</span>
        <span>{problem.length} / 500</span>
      </div>

    </div>

    <button
      className="start-btn"
      onClick={() => setPage("advice")}
    >
      💀 GIVE ME TERRIBLE ADVICE
    </button>

    <p className="warning">
      ⚠ WARNING: The committee accepts no responsibility for your decisions.
    </p>

  </main>
)}

      {/* ADVICE PAGE */}
{page === "advice" && (
  <main className="advice-page">

    <div className="welcome-tag">
      ☠ THE COMMITTEE HAS SPOKEN
    </div>

    <h1>
      YOUR PROBLEM IS NOW <span>WORSE</span>
    </h1>

    <p className="subtitle">
      Three experts. Three terrible solutions. Choose wisely.
    </p>
    <div className="worst-winner">
  🏆 CURRENT WORST ADVISOR: <strong>REDDIT MAMAN</strong>
</div>

    <div className="advice-list">

      {/* CHECHI */}
      <div className={`advice-card chechi-advice ${ignored === "chechi" ? "ignored" : ""}`}>
        <img
  className="advice-character-image"
  src="/src/assets/chechi.png"
  alt="Chechi"
/>
        <div className="advice-top">
          <h2>👩 CHECHI</h2>
          <span>BADNESS: 86%</span>
        </div>

        <p>
          "Don't study. Just look at the textbook very confidently.
          Your brain will absorb the knowledge through eye contact."
        </p>

        <small>☠ EMOTIONAL EXPERT</small>
       <button
  className="ignore-btn"
  onClick={() => setIgnored(ignored === "chechi" ? "" : "chechi")}
>
  {ignored === "chechi" ? "↩ UNDO" : "🚫 IGNORE CHECHI"}
</button>
      </div>


      {/* UPADESHI */}
      <div className={`advice-card upadeshi-advice ${ignored === "upadeshi" ? "ignored" : ""}`}>
        <img
  className="advice-character-image"
  src="/src/assets/nattile updeshi.png"
  alt="Nattile Upadeshi"
/>
        <div className="advice-top">
          <h2>🧓 NATTILE UPADESHI</h2>
          <span>BADNESS: 94%</span>
        </div>

        <p>
          "Wake up at 4 AM, stare at the ceiling for one hour,
          and then go back to sleep. Your subconscious will study."
        </p>

        <small>☠ UNSOLICITED EXPERT</small>
        <button
  className="ignore-btn"
  onClick={() => setIgnored(ignored === "upadeshi" ? "" : "upadeshi")}
>
  {ignored === "upadeshi" ? "↩ UNDO" : "🚫 IGNORE UPADESHI"}
</button>
      </div>


      {/* REDDIT MAMAN */}
      <div className={`advice-card reddit-advice ${ignored === "reddit_maman" ? "ignored" : ""}`}>
        <img
  className="advice-character-image"
  src={redditImage}
  alt="Reddit Maman"
/>
        <div className="advice-top">
          <h2>🕶️ REDDIT MAMAN</h2>
          <span>BADNESS: 99%</span>
        </div>

        <p>
          "Bro, someone on Reddit solved this by doing absolutely
          nothing. Trust me, bro. It had 47 upvotes."
        </p>

        <small>☠ INTERNET EXPERT</small>
        <button
  className="ignore-btn"
  onClick={() => setIgnored(ignored === "reddit_maman" ? "" : "reddit_maman")}
>
  {ignored === "reddit_maman" ? "↩ UNDO" : "🚫 IGNORE REDDIT MAMAN"}
</button>
      </div>

    </div>
    <button
  className="argue-btn"
  onClick={() => setPage("argument")}
>
  ⚔️ MAKE THEM ARGUE
</button>
<button
  className="why-btn"
  onClick={() => setPage("why")}
>
 
  🧠 WHY DID THEY SAY THIS?
</button>


        <div className="advice-actions">

      <button
        className="start-btn"
        onClick={() => setPage("worse")}
      >
        🔥 MAKE IT WORSE
      </button>

      <button
        className="back-btn"
        onClick={() => setPage("chat")}
      >
        ← TRY ANOTHER PROBLEM
      </button>

    </div>

  </main>
)}
      {/* ARGUMENT PAGE */}
{page === "argument" && (
  <main className="argument-page">

    <div className="welcome-tag">
      ⚔️ COMMITTEE CIVIL WAR
    </div>

    <h1>
      THEY'RE <span>ARGUING</span>
    </h1>

    <p className="subtitle">
      Three terrible opinions. One extremely unnecessary argument.
    </p>

    <div className="argument-box">

      <div className="argument-line">
        <strong>👩 CHECHI:</strong>
        <p>"Obviously my advice was the best. I have experience."</p>
      </div>

      <div className="argument-line">
        <strong>🧓 NATTILE UPADESHI:</strong>
        <p>"Experience? I once gave advice to someone in 1998."</p>
      </div>

      <div className="argument-line">
        <strong>🕶️ REDDIT MAMAN:</strong>
        <p>"Bro, both of you are wrong. Reddit agrees with me."</p>
      </div>

      <div className="argument-line final-argument">
        <strong>☠ COMMITTEE VERDICT:</strong>
        <p>Nobody won. Everyone became more confident.</p>
      </div>

    </div>
    <button
  className="back-btn"
  onClick={() => setPage("advice")}
>
  ← BACK TO ADVICE
</button>

    

  </main>
)}

      {/* WORSE PAGE */}
      {page === "worse" && (
        <main className="worse-page">

          <div className="welcome-tag">
            ☠ CONSEQUENCES DEPARTMENT
          </div>

          <h1>
            YOU MADE THE <span>WRONG CHOICE</span>
          </h1>

          <p className="subtitle">
            Congratulations. Your problem has officially become worse.
          </p>

          <div className="chaos-box">

  <div className="chaos-title">
    💀 CONSEQUENCE CHAIN
  </div>

  <div className="consequence">
    <strong>STEP 1</strong>
    <p>You stop studying.</p>
  </div>

  <div className="arrow">↓</div>

  <div className="consequence">
    <strong>STEP 2</strong>
    <p>You become extremely confident for absolutely no reason.</p>
  </div>

  <div className="arrow">↓</div>

  <div className="consequence">
    <strong>STEP 3</strong>
    <p>You enter the exam hall with nothing in your brain.</p>
  </div>

  <div className="arrow">↓</div>

  <div className="consequence final-consequence">
    <strong>☠ FINAL CONSEQUENCE</strong>
    <p>You write your name beautifully and consider that a good start.</p>
  </div>

</div>

          

          <button
            className="back-btn"
            onClick={() => setPage("dashboard")}
          >
            ← BACK TO SAFETY
          </button>

        </main>
      )}
      {/* WHY PAGE */}
{page === "why" && (
  <main className="why-page">

    <div className="welcome-tag">
      🧠 AI INVESTIGATION DEPARTMENT
    </div>

    <h1>
      WHY DID THEY <span>SAY THIS?</span>
    </h1>

    <p className="subtitle">
      We investigated their reasoning. We immediately regretted it.
    </p>

    <div className="reason-box">

      <div className="reason">
        <strong>👩 CHECHI</strong>
        <p>
          The AI detected the word "exam" and decided that
          studying was probably the problem.
        </p>
      </div>

      <div className="reason">
        <strong>🧓 NATTILE UPADESHI</strong>
        <p>
          The system retrieved an extremely questionable
          piece of advice and decided to make it worse.
        </p>
      </div>

      <div className="reason">
        <strong>🕶️ REDDIT MAMAN</strong>
        <p>
          A Reddit post with suspicious confidence was found.
          The AI trusted it for absolutely no reason.
        </p>
      </div>

      <div className="reason final-reason">
        <strong>☠ AI CONCLUSION</strong>
        <p>
          The advice makes no sense. Therefore, it is perfect
          for this committee.
        </p>
      </div>

    </div>

    <button
      className="back-btn"
      onClick={() => setPage("advice")}
    >
      ← BACK TO ADVICE
    </button>

  </main>
)}

    </div>
  );
}

export default App;