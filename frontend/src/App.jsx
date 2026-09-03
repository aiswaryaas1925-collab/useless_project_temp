import { useState } from "react";
import "./App.css";
import redditImage from "./assets/redditmaman.png";
function App() {
 const [page, setPage] = useState("dashboard");
 const [ignored, setIgnored] = useState("");

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

          <button>☠ Hall of Shame</button>
          <button>⚙ Why this exists?</button>
          <button>ⓘ About</button>
        </div>

        <div className="nav-right">
          <button>🔊</button>
          <button>മലയാളം⌄</button>
        </div>

      </nav>


      {/* DASHBOARD */}
      {page === "dashboard" && (
        <main className="dashboard">

          <div className="welcome-tag">
            ☠ WELCOME TO THE COMMITTEE
          </div>

          <h1>
            MEET YOUR <span>ADVISORS</span>
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
      />

      <div className="input-footer">
        <span>⚠ Your problem will be made significantly worse.</span>
        <span>0 / 500</span>
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


    <div className="advice-actions">

      <button
        className="start-btn"
        onClick={() => setPage("advice")}
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

    </div>
  );
}

export default App;