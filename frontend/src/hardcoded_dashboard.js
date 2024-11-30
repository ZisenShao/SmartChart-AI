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

  const toggleMode = () => {
    setIsFriendlyMode((prevMode) => !prevMode);
  };

  return (
    <div className="dashboard-container">
      <div className="toggle-container">
        <label className="switch">
          <input
            type="checkbox"
            checked={isFriendlyMode}
            onChange={toggleMode}
          />
          <span className="slider"></span>
        </label>
        <span className="toggle-label">
          {isFriendlyMode ? "Friendly Mode" : "Default Mode"}
        </span>
      </div>

      <h1 className="clinical-notes-heading">
        {isFriendlyMode ? "Detailed Clinical Notes" : "General Information"}
      </h1>

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
          <div className="card">
            <h3>
              <img src={magnifyingGlass} alt="Diagnosis" className="icon" />
              Diagnosis
            </h3>
            <p>
              "You have heart disease that sometimes causes chest pain, but it’s
              stable and manageable."
            </p>
          </div>

          <div className="card">
            <h3>
              <img src={warning} alt="Symptoms" className="icon" />
              Symptoms You May Experience
            </h3>
            <p>
              Chest pain during activity, relieved by rest. No nausea,
              dizziness, or other symptoms.
            </p>
          </div>

          <div className="card">
            <h3>
              <img src={pill} alt="Medications" className="icon" />
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
              <img src={clipboard} alt="Key Tests" className="icon" />
              Key Test Results
            </h3>
            <p>Blood Pressure: 142/88 mmHg (slightly high)</p>
            <p>Cholesterol: 210 mg/dL (high cholesterol)</p>
            <p>Stress Test: Reduced blood flow to the heart was found.</p>
          </div>

          <div className="card">
            <h3>
              <img src={food} alt="Heart Tips" className="icon" />
              Tips for a Healthy Heart
            </h3>
            <p>
              Eat a low-sodium and low-cholesterol diet. Avoid smoking. Join a
              cardiac rehabilitation program.
            </p>
          </div>

          <div className="card">
            <h3>
              <img src={group} alt="Next Steps" className="icon" />
              Your Next Steps
            </h3>
            <p>
              Get a heart test (angiogram) on October 5th, 2024. Follow up with
              your heart doctor in 2 weeks.
            </p>
          </div>
        </div>
      ) : (
        <div className="cards-container">
          <div className="card">
            <h3>
              <img src={magnifyingGlass} alt="Diagnosis" className="icon" />
              Diagnosis
            </h3>
            <p>
              The patient exhibits clinical manifestations consistent with
              ischemic heart disease, characterized by episodic angina pectoris
              likely due to coronary artery stenosis. Current status is stable,
              warranting continued pharmacologic management.
            </p>
          </div>

          <div className="card">
            <h3>
              <img src={warning} alt="Symptoms" className="icon" />
              Symptoms You May Experience
            </h3>
            <p>
              Patients may experience exertional angina, typically manifesting
              as substernal chest discomfort that subsides with cessation of
              activity. Absence of autonomic symptoms, including diaphoresis or
              syncope, is noted.
            </p>
          </div>

          <div className="card">
            <h3>
              <img src={pill} alt="Medications" className="icon" />
              Medications Prescribed
            </h3>
            <ul>
              <li>
                Aspirin 81 mg, q.d. - an antiplatelet agent for the prevention
                of thrombotic cardiovascular events.
              </li>
              <li>
                Atorvastatin 40 mg, q.d. - a statin indicated for hyperlipidemia
                management and plaque stabilization.
              </li>
              <li>
                Metoprolol 25 mg, b.i.d. - a beta-blocker prescribed for rate
                control and myocardial ischemic prophylaxis.
              </li>
              <li>
                Nitroglycerin 0.4 mg PRN - a nitrate for acute angina relief.
              </li>
            </ul>
          </div>

          <div className="card">
            <h3>
              <img src={clipboard} alt="Key Tests" className="icon" />
              Key Test Results
            </h3>
            <p>
              Blood Pressure: 142/88 mmHg - Hypertensive range, warranting
              ongoing monitoring.
            </p>
            <p>
              Total Cholesterol: 210 mg/dL - Dyslipidemia requiring lifestyle
              and pharmacologic intervention.
            </p>
            <p>
              Stress Test: Positive for inducible ischemia, indicating
              myocardial perfusion deficits.
            </p>
          </div>

          <div className="card">
            <h3>
              <img src={food} alt="Heart Tips" className="icon" />
              Lifestyle Recommendations
            </h3>
            <p>
              Adherence to a sodium-restricted, low-cholesterol diet is
              recommended to reduce cardiovascular morbidity risk. Smoking
              cessation and participation in a structured cardiac rehabilitation
              program are advised.
            </p>
          </div>

          <div className="card">
            <h3>
              <img src={group} alt="Next Steps" className="icon" />
              Next Steps in Care
            </h3>
            <p>
              Schedule an angiographic evaluation (coronary angiogram) on
              October 5, 2024, to assess coronary patency. A follow-up
              consultation is recommended within 2 weeks post-procedure.
            </p>
          </div>
        </div>
      )}
    </div>
  );
};