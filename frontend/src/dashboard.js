import React, { useState, useEffect } from "react";
import axios from 'axios';
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
    const [medicalReport, setMedicalReport] = useState({
        default: null,
        friendly: null
    });
    const [isLoading, setIsLoading] = useState(true);
    const [friendlyCards, setFriendlyCards] = useState([]);

    useEffect(() => {
        const fetchMedicalReport = async () => {
            try {
                console.log('Fetching medical report...');
                const response = await axios.get('http://localhost:8000/api/read_medical_report/');

                const txtResponse = await fetch('/reports/john_davis_report.txt');
                const txtContent = await txtResponse.text();

                if (response.data.success) {
                    setMedicalReport({
                        default: {
                            ...response.data.medicalReport,
                            txtContent
                        },
                        friendly: null
                    });
                    setIsLoading(false);
                }
            } catch (error) {
                console.error('Error fetching medical report:', error.response || error.message || error);
                setIsLoading(false);
            }
        };

        fetchMedicalReport();
    }, []);

    const toggleMode = async () => {
        if (!isFriendlyMode && !medicalReport.friendly) {
            try {
                const response = await axios.post('http://localhost:8000/api/convert_to_friendly_mode/', {
                    medicalReport: JSON.stringify(medicalReport.default)
                });

                if (response.data.success) {
                    // Parse the friendly report into cards
                    const friendlyText = response.data.friendlyReport;
                    const cardSections = [
                        {
                            title: "Diagnosis",
                            icon: magnifyingGlass,
                            content: extractSection(friendlyText, "Diagnosis")
                        },
                        {
                            title: "Symptoms You May Experience",
                            icon: warning,
                            content: extractSection(friendlyText, "Symptoms")
                        },
                        {
                            title: "Medications You Should Take",
                            icon: pill,
                            content: extractSection(friendlyText, "Medications")
                        },
                        {
                            title: "Key Test Results",
                            icon: clipboard,
                            content: extractSection(friendlyText, "Test Results")
                        },
                        {
                            title: "Tips for a Healthy Heart",
                            icon: food,
                            content: extractSection(friendlyText, "Health Tips")
                        },
                        {
                            title: "Your Next Steps",
                            icon: group,
                            content: extractSection(friendlyText, "Next Steps")
                        }
                    ];

                    setFriendlyCards(cardSections);
                    setMedicalReport(prev => ({
                        ...prev,
                        friendly: friendlyText
                    }));
                }
            } catch (error) {
                console.error('Error converting to friendly mode:', error);
            }
        }

        setIsFriendlyMode((prevMode) => !prevMode);
    };

    // Helper function to extract sections from the friendly report
    const extractSection = (text, sectionTitle) => {
        const regex = new RegExp(`(?<=${sectionTitle}:)(.*?)(?=(\\n[A-Z][a-z]|$))`, 's');
        const match = text.match(regex);

        if (match) {
            return match[1].trim()
                .replace(/\n+/g, ' ')
                .replace(/\s+/g, ' ')
                .trim();
        }

        return "Information not available";
    };

    if (isLoading) {
        return <div>Loading...</div>;
    }

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

            {medicalReport.default ? (
                <div className="patient-info">
                    <p>
                        <img src={person} alt="Person Icon" className="icon" />
                        Patient Name: {medicalReport.default.patient.name || "N/A"}
                    </p>
                    <p>
                        <img src={stethoscope} alt="Stethoscope Icon" className="icon" />
                        Date of Visit: {medicalReport.default.patient.date_of_service || "N/A"}
                    </p>
                    <p>
                        <img src={stethoscope} alt="Provider Icon" className="icon" />
                        Provider: {medicalReport.default.patient.provider || "N/A"}
                    </p>
                </div>
            ) : (
                <div>Loading patient info...</div>
            )}

            {isFriendlyMode ? (
                <div className="cards-container">
                    {friendlyCards.map((card, index) => (
                        <div key={index} className="card">
                            <h3>
                                <img src={card.icon} alt={card.title} className="icon" />
                                {card.title}
                            </h3>
                            <p>{card.content}</p>
                        </div>
                    ))}
                </div>
            ) : (
                <div className="full-report-container">
                    <pre style={{
                        whiteSpace: 'pre-wrap',
                        textAlign: 'left',
                        width: '100%',
                        fontFamily: 'Arial, sans-serif',
                        lineHeight: '1.6',
                        padding: '20px',
                        backgroundColor: '#f9f9f9',
                        borderRadius: '8px',
                        overflowX: 'auto'
                    }}>
                        {medicalReport && medicalReport.default && medicalReport.default.txtContent ? (
                            <pre style={{
                                whiteSpace: 'pre-wrap',
                                textAlign: 'left',
                                width: '100%',
                                fontFamily: 'Arial, sans-serif',
                                lineHeight: '1.6',
                                padding: '20px',
                                backgroundColor: '#f9f9f9',
                                borderRadius: '8px',
                                overflowX: 'auto'
                            }}>
                                {medicalReport.default.txtContent}
                            </pre>
                        ) : (
                            <p>No report available</p>
                        )}
                    </pre>
                </div>
            )}
        </div>
    );

};

export default Dashboard;