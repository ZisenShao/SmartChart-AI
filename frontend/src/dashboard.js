import React, { useState } from "react";
import clipboard from "./dashboard assets/Clipboard.svg";
import food from "./dashboard assets/Food.svg";
import group from "./dashboard assets/Group.svg";
import magnifyingGlass from "./dashboard assets/Magnifying Glass.svg";
import noSmoking from "./dashboard assets/nosmoking.svg";
import pill from "./dashboard assets/Pill.svg";
import stethoscope from "./dashboard assets/Stethoscope.svg";
import vector from "./dashboard assets/Vector.svg";
import warning from "./dashboard assets/Warning.svg";
import person from "./dashboard assets/person.svg";
import "./dashboard.css";

const Dashboard = () => {
  const [isFriendlyMode, setIsFriendlyMode] = useState(false);

  // Toggle between friendly and default mode
  const toggleMode = () => {
    setIsFriendlyMode((prevMode) => !prevMode);
  };

  return (
    <div className="dashboard-container">
      <div className="toggle-container">
        <button className={`toggle-option ${isFriendlyMode ? "" : "active"}`} onClick={toggleMode}>
          {isFriendlyMode ? "Default Mode" : "Friendly Mode"}
        </button>
      </div>

      <h1 className="clinical-notes-heading">{isFriendlyMode ? "Detailed Clinical Notes" : "General Information"}</h1>

      <div className="patient-info">
        <p>
          <img src={person} alt="Person Icon" className="icon" />
          Patient Name: John Davis
        </p>
        <p>
          <img src={stethoscope} alt="Stethoscope Icon" className="icon" />
          Date of Visit: 09/30/2024
        </p>
        <p>
          <img src={stethoscope} alt="Provider Icon" className="icon" />
          Provider: Dr. Jane Smith, Cardiologist
        </p>
      </div>

      {isFriendlyMode ? (
        <div className="cards-container">
          {/* All detailed cards go here */}
          <div className="card">
            <h3>
              <img src={magnifyingGlass} alt="Magnifying Glass Icon" className="icon" />
              Diagnosis
            </h3>
            <p>"You have heart disease that sometimes causes chest pain, but it’s stable and manageable."</p>
          </div>

          <div className="card warning">
            <h3>
              <img src={warning} alt="Warning Icon" className="icon" />
              Symptoms You May Experience
            </h3>
            <p>Chest pain during activity, relieved by rest. No nausea, dizziness, or other symptoms.</p>
          </div>

          <div className="card">
            <h3>
              <img src={pill} alt="Pill Icon" className="icon" />
              Medications You Should Take
            </h3>
            <ul>
              <li>Aspirin (81 mg, once daily)</li>
              <li>Atorvastatin (40 mg, once daily)</li>
              <li>Metoprolol (25 mg, twice daily)</li>
              <li>Nitroglycerin (0.4 mg)</li>
            </ul>
          </div>

          <div className="card">
            <h3>
              <img src={clipboard} alt="Clipboard Icon" className="icon" />
              Key Test Results
            </h3>
            <p>Blood Pressure: 142/88 mmHg (slightly high)</p>
            <p>Cholesterol: 210 mg/dL (high cholesterol)</p>
            <p>Stress Test: Reduced blood flow to the heart was found.</p>
          </div>

          <div className="card">
            <h3>
              <img src={food} alt="Food Icon" className="icon" />
              Tips for a Healthy Heart
            </h3>
            <p>Eat a low-sodium and low-cholesterol diet. Avoid smoking. Join a cardiac rehabilitation program.</p>
          </div>

          <div className="card">
            <h3>
              <img src={group} alt="Group Icon" className="icon" />
              Your Next Steps
            </h3>
            <p>Get a heart test (angiogram) on October 5th, 2024. Follow up with your heart doctor in 2 weeks.</p>
          </div>
        </div>
      ) : (
        <div className="simple-info">
          <h2>Welcome to Default Mode</h2>
          <p>Details to be added here...</p>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
