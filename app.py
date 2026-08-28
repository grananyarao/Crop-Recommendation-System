
import streamlit as st
import pandas as pd
import joblib
from pathlib import Path

# PAGE CONFIGURATION

st.set_page_config(
    page_title="Smart Agriculture Advisory",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown(
    """
<style>

/* ============================================================
   LIGHT GREEN THEME
   ============================================================ */

:root {
  --bg: #f4faf4;
  --bg2: #e8f5e9;
  --primary: #2e7d32;
  --secondary: #43a047;
  --accent: #7cb342;
  --text: #1b4332;
  --muted: #52705b;
  --card: rgba(255, 255, 255, 0.92);
  --border: rgba(46, 125, 50, 0.18);
  --shadow: 0 12px 35px rgba(46, 125, 50, 0.10);
}


/* ============================================================
   GLOBAL
   ============================================================ */

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html {
  scroll-behavior: smooth;
}

body {
  font-family: Arial, sans-serif;
  color: var(--text);
  background:
    radial-gradient(
      circle at top left,
      rgba(124, 179, 66, 0.15),
      transparent 25%
    ),
    radial-gradient(
      circle at top right,
      rgba(67, 160, 71, 0.12),
      transparent 25%
    ),
    linear-gradient(
      135deg,
      var(--bg),
      var(--bg2)
    );
  overflow-x: hidden;
  min-height: 100vh;
}

a {
  text-decoration: none;
  color: inherit;
}

img {
  width: 100%;
  display: block;
  border-radius: 20px;
}

.container {
  width: min(1180px, 92%);
  margin: 0 auto;
}


/* ============================================================
   CURSOR GLOW
   ============================================================ */

.cursor-glow {
  width: 320px;
  height: 320px;
  position: fixed;
  left: 0;
  top: 0;
  pointer-events: none;
  border-radius: 50%;
  background:
    radial-gradient(
      circle,
      rgba(124, 179, 66, 0.15),
      transparent 65%
    );
  transform: translate(-50%, -50%);
  z-index: 0;
  filter: blur(10px);
}


/* ============================================================
   HEADER
   ============================================================ */

.site-header {
  position: sticky;
  top: 0;
  z-index: 999;
  background: rgba(255, 255, 255, 0.94);
  border-bottom: 1px solid rgba(46, 125, 50, 0.12);
  backdrop-filter: blur(10px);
}

.nav {
  min-height: 82px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
}

.brand {
  display: flex;
  align-items: center;
  gap: 14px;
}

.brand-logo {
  width: 52px;
  height: 52px;
  border-radius: 18px;
  display: grid;
  place-items: center;
  font-size: 1.3rem;
  font-weight: 800;
  color: #ffffff;
  background: linear-gradient(
    135deg,
    var(--primary),
    var(--secondary)
  );
}

.brand h3,
.brand p,
.nav-links a,
.hero h1,
.hero-description,
.section-title h2,
.section-title p,
.glass-card h3,
.glass-card p,
.feature-card h3,
.feature-card p,
.future-card h3,
.future-card p,
.team-card h3,
.team-card p,
.arch-card h3,
.arch-card p,
.guide-card h3,
.guide-card p,
.timeline-content h3,
.timeline-content p,
.visual-top,
.mini-box,
.mini-core,
.mini-row span,
.tech-pill {
  color: var(--text);
}

.nav-links {
  display: flex;
  gap: 24px;
}

.nav-links a:hover {
  color: var(--primary);
}


/* ============================================================
   BUTTONS
   ============================================================ */

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 48px;
  padding: 14px 24px;
  border-radius: 999px;
  font-weight: 700;
  transition: 0.3s ease;
}

.btn-primary {
  background: linear-gradient(
    135deg,
    var(--primary),
    var(--secondary)
  );
  color: #ffffff;
}

.btn-secondary {
  border: 1px solid var(--border);
  background: rgba(255, 255, 255, 0.75);
  color: var(--primary);
}


/* ============================================================
   HERO
   ============================================================ */

.hero {
  min-height: 100vh;
  display: flex;
  align-items: center;
  padding: 80px 0 40px;
  position: relative;
  overflow: hidden;
}

.hero-bg-grid {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(
      rgba(46, 125, 50, 0.05) 1px,
      transparent 1px
    ),
    linear-gradient(
      90deg,
      rgba(46, 125, 50, 0.05) 1px,
      transparent 1px
    );
  background-size: 60px 60px;
  opacity: 0.5;
}

.floating {
  position: absolute;
  border-radius: 50%;
  filter: blur(10px);
  animation: floatBlob 8s ease-in-out infinite;
}

.floating-1 {
  width: 220px;
  height: 220px;
  background: rgba(124, 179, 66, 0.15);
  top: 12%;
  left: 6%;
}

.floating-2 {
  width: 280px;
  height: 280px;
  background: rgba(67, 160, 71, 0.12);
  bottom: 10%;
  right: 5%;
  animation-delay: 1.5s;
}

.floating-3 {
  width: 160px;
  height: 160px;
  background: rgba(174, 213, 129, 0.18);
  top: 18%;
  right: 25%;
  animation-delay: 3s;
}

@keyframes floatBlob {
  0%, 100% {
    transform: translateY(0) translateX(0) scale(1);
  }
  50% {
    transform: translateY(-24px) translateX(10px) scale(1.08);
  }
}

.hero-content {
  display: grid;
  gap: 50px;
  align-items: center;
  position: relative;
  z-index: 2;
}

.hero-single {
  grid-template-columns: 1fr;
  max-width: 760px;
  margin-left: 0;
}

.hero-text {
  max-width: 760px;
  padding-left: 42px;
}

.eyebrow {
  display: inline-block;
  margin-bottom: 18px;
  color: var(--primary);
  letter-spacing: 0.14em;
  text-transform: uppercase;
  font-size: 0.85rem;
  font-weight: 700;
}

.hero h1 {
  font-size: clamp(2.8rem, 7vw, 5.5rem);
  line-height: 1.05;
  margin-bottom: 20px;
  color: #163d20;
}

.hero h1 span {
  color: var(--primary);
}

.hero-description,
.section-title p {
  font-size: 1.05rem;
  line-height: 1.8;
  max-width: 680px;
  color: var(--muted);
}

.centered-section-text {
  max-width: 820px;
  margin: 0 auto;
  text-align: center;
}

.hero-actions {
  display: flex;
  gap: 16px;
  margin: 28px 0 34px;
  flex-wrap: wrap;
}


/* ============================================================
   CARDS
   ============================================================ */

.glass-card,
.feature-card,
.future-card,
.team-card,
.arch-card,
.workflow-card,
.guide-card,
.tech-pill,
.timeline-content {
  background: var(--card);
  border: 1px solid var(--border);
  box-shadow: var(--shadow);
  border-radius: 24px;
}

.section {
  padding: 100px 0;
}

.section-title {
  text-align: center;
  margin-bottom: 56px;
}

.section-title h2 {
  font-size: clamp(2rem, 5vw, 3.2rem);
  margin-bottom: 16px;
}

.about-grid,
.future-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}

.team-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
}

.glass-card,
.feature-card,
.future-card,
.team-card {
  padding: 28px;
  transition: 0.3s ease;
}


/* ============================================================
   ARCHITECTURE
   ============================================================ */

.architecture-only-layout {
  display: grid;
  grid-template-columns: 1.1fr 0.9fr;
  gap: 28px;
  align-items: start;
  max-width: 1100px;
  margin: 0 auto;
}

.architecture-points {
  display: grid;
  gap: 18px;
}

.workflow-card {
  padding: 24px;
  height: fit-content;
}

.arch-card {
  display: flex;
  gap: 18px;
  padding: 24px;
}

.arch-card span {
  min-width: 54px;
  height: 54px;
  border-radius: 50%;
  display: grid;
  place-items: center;
  font-weight: 700;
  color: #ffffff;
  background: linear-gradient(
    135deg,
    var(--primary),
    var(--accent)
  );
}

.visual-top {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 18px;
}

.pulse-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: var(--primary);
}

.mini-flow {
  display: grid;
  gap: 14px;
}

.mini-box,
.mini-core,
.mini-row span,
.tech-pill {
  border-radius: 18px;
  padding: 16px;
  text-align: center;
}

.mini-box {
  background: rgba(124, 179, 66, 0.10);
  border: 1px solid rgba(46, 125, 50, 0.20);
}

.mini-core {
  background: rgba(67, 160, 71, 0.10);
  border: 1px solid rgba(67, 160, 71, 0.20);
  font-weight: 700;
}

.mini-arrow {
  text-align: center;
  font-size: 1.5rem;
  color: var(--primary);
}

.mini-row {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.mini-row span {
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid var(--border);
}


/* ============================================================
   TIMELINE
   ============================================================ */

.timeline {
  position: relative;
  max-width: 900px;
  margin: 0 auto;
}

.timeline::before {
  content: "";
  position: absolute;
  left: 22px;
  top: 0;
  width: 4px;
  height: 100%;
  background: linear-gradient(
    var(--primary),
    var(--secondary),
    var(--accent)
  );
  border-radius: 999px;
}

.timeline-item {
  position: relative;
  padding-left: 74px;
  margin-bottom: 36px;
}

.timeline-dot {
  position: absolute;
  left: 10px;
  top: 8px;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: radial-gradient(
    circle,
    var(--accent),
    var(--primary)
  );
}

.timeline-content {
  padding: 26px;
}


/* ============================================================
   TECHNOLOGY
   ============================================================ */

.tech-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  justify-content: center;
}

.tech-pill {
  padding: 18px 24px;
  font-weight: 700;
}


/* ============================================================
   GUIDE
   ============================================================ */

.guide-card {
  margin-top: 26px;
  padding: 24px;
  text-align: center;
}

.reveal {
  opacity: 1;
  transform: none;
}

.reveal.active {
  opacity: 1;
  transform: none;
}

.tilt {
  transform: none;
}


/* ============================================================
   RESPONSIVE
   ============================================================ */

@media (max-width: 1100px) {

  .architecture-only-layout {
    grid-template-columns: 1fr;
  }

  .about-grid,
  .features-grid,
  .future-grid,
  .team-grid {
    grid-template-columns: 1fr 1fr;
  }

  .nav-links {
    display: none;
  }
}

@media (max-width: 768px) {

  .hero {
    padding-top: 40px;
  }

  .about-grid,
  .features-grid,
  .future-grid,
  .team-grid {
    grid-template-columns: 1fr;
  }

  .hero-actions {
    display: flex;
    flex-direction: column;
  }

  .btn {
    width: 100%;
  }

  .section {
    padding: 80px 0;
  }

  .site-header {
    position: relative;
  }

  .hero-single {
    max-width: 100%;
  }

  .hero-text {
    padding-left: 14px;
    padding-right: 14px;
  }
}


/* ============================================================
   DEMO SECTION
   ============================================================ */

.demo-section .section-title {
  margin-bottom: 40px;
}

.demo-layout {
  display: grid;
  grid-template-columns: minmax(0, 1.1fr) minmax(0, 0.9fr);
  gap: 28px;
  align-items: flex-start;
}

.demo-form {
  padding: 28px;
}

.demo-form h3 {
  margin-bottom: 18px;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px 20px;
  margin-bottom: 20px;
}

.form-grid label {
  display: flex;
  flex-direction: column;
  font-size: 0.9rem;
  color: var(--muted);
  gap: 6px;
}

.form-grid span {
  font-weight: 500;
  color: var(--text);
}

.form-grid input {
  border-radius: 999px;
  border: 1px solid var(--border);
  background: #ffffff;
  padding: 10px 14px;
  color: var(--text);
  outline: none;
}

.form-grid input:focus {
  border-color: var(--primary);
  box-shadow:
    0 0 0 1px rgba(46, 125, 50, 0.35);
}

.demo-btn {
  width: 100%;
  margin-top: 4px;
}

.demo-error {
  margin-top: 10px;
  color: #c62828;
  font-size: 0.9rem;
  min-height: 1.2em;
}

.demo-result {
  padding: 28px;
}

.demo-result h3 {
  margin-bottom: 10px;
}

.demo-hint {
  color: var(--muted);
  font-size: 0.95rem;
  margin-bottom: 18px;
}

.demo-main-result {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 16px;
}

.demo-label {
  font-size: 0.95rem;
  color: var(--muted);
}

.demo-value {
  font-family: "Orbitron", sans-serif;
  font-size: 1.8rem;
  color: var(--primary);
}

.demo-top3 h4 {
  margin-bottom: 8px;
}

.demo-top3 ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  gap: 6px;
}

.demo-top3 li {
  display: flex;
  justify-content: space-between;
  font-size: 0.95rem;
  color: var(--muted);
}

.demo-top3 li span:first-child {
  color: var(--text);
}

@media (max-width: 900px) {

  .demo-layout {
    grid-template-columns: 1fr;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }
}


/* ============================================================
   WEATHER SECTION
   ============================================================ */

.weather-section .section-title {
  margin-bottom: 40px;
}

.weather-layout {
  display: grid;
  grid-template-columns: 1fr;
  gap: 24px;
  align-items: flex-start;
}

.weather-form {
  padding: 26px 24px;
}

.weather-form h3 {
  margin-bottom: 16px;
}

.weather-label {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-bottom: 16px;
  font-size: 0.9rem;
  color: var(--muted);
}

.weather-label span {
  font-weight: 500;
  color: var(--text);
}

.weather-label input {
  border-radius: 999px;
  border: 1px solid var(--border);
  background: #ffffff;
  padding: 10px 14px;
  color: var(--text);
  outline: none;
}

.weather-label input:focus {
  border-color: var(--secondary);
  box-shadow:
    0 0 0 1px rgba(67, 160, 71, 0.35);
}

.weather-btn {
  width: 100%;
  margin-top: 4px;
}

.weather-error {
  margin-top: 10px;
  color: #c62828;
  font-size: 0.9rem;
  min-height: 1.2em;
}

.weather-result {
  padding: 26px 24px;
}

.weather-result h3 {
  margin-bottom: 10px;
}

.weather-hint {
  color: var(--muted);
  font-size: 0.95rem;
  margin-bottom: 18px;
}

.weather-main {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 18px;
  gap: 14px;
}

.weather-city {
  font-size: 1.1rem;
  font-weight: 600;
}

.weather-description {
  font-size: 0.95rem;
  color: var(--muted);
  text-transform: capitalize;
}

.weather-temp-block {
  display: flex;
  align-items: baseline;
  gap: 4px;
}

.weather-temp {
  font-family: "Orbitron", sans-serif;
  font-size: 2.2rem;
  color: var(--primary);
}

.weather-unit {
  font-size: 0.9rem;
  color: var(--muted);
}

.weather-stats {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
  margin-bottom: 18px;
}

.weather-stat {
  padding: 12px 10px;
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.75);
  border: 1px solid var(--border);
}

.weather-stat-label {
  display: block;
  font-size: 0.8rem;
  color: var(--muted);
  margin-bottom: 4px;
}

.weather-stat-value {
  font-size: 0.95rem;
  font-weight: 600;
}

.weather-advisory-block {
  margin-top: 8px;
}

.weather-advisory-block h4 {
  margin-bottom: 4px;
}

.weather-advice-text {
  font-size: 0.95rem;
  color: var(--muted);
  line-height: 1.6;
}

@media (max-width: 900px) {

  .weather-layout {
    grid-template-columns: 1fr;
  }

  .weather-stats {
    grid-template-columns: 1fr;
  }
}


/* ============================================================
   DISEASE DETECTION SECTION
   ============================================================ */

.disease-section .section-title {
  margin-bottom: 40px;
}

.disease-layout {
  display: grid;
  grid-template-columns: minmax(0, 1.1fr) minmax(0, 0.9fr);
  gap: 28px;
  align-items: flex-start;
}

.disease-form {
  padding: 28px;
}

.disease-form h3,
.disease-result h3 {
  margin-bottom: 16px;
}

.file-drop {
  display: block;
  border: 1.5px dashed rgba(46, 125, 50, 0.35);
  border-radius: 24px;
  padding: 28px 22px;
  cursor: pointer;
  transition:
    border-color 0.25s ease,
    background 0.25s ease,
    transform 0.25s ease;
  margin-bottom: 20px;
  background:
    radial-gradient(
      circle at top left,
      rgba(124, 179, 66, 0.12),
      transparent 55%
    );
}

.file-drop-inner {
  text-align: center;
}

.file-drop-title {
  font-size: 1rem;
  font-weight: 700;
  color: var(--text);
  margin-bottom: 6px;
}

.file-drop-hint {
  font-size: 0.92rem;
  color: var(--muted);
  opacity: 0.9;
}

.file-drop:hover,
.file-drop.file-drop--active {
  border-color: var(--primary);
  background:
    radial-gradient(
      circle at top left,
      rgba(124, 179, 66, 0.18),
      transparent 60%
    );
  transform: translateY(-1px);
}

.preview-wrapper {
  margin-bottom: 20px;
}

.preview-label {
  font-size: 0.9rem;
  color: var(--muted);
  margin-bottom: 8px;
}

.preview-box {
  border-radius: 24px;
  border: 1px solid var(--border);
  background: rgba(255, 255, 255, 0.75);
  min-height: 240px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  position: relative;
}

.preview-placeholder {
  font-size: 0.95rem;
  color: var(--muted);
}

#preview-image {
  display: none;
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 0;
}

.disease-btn {
  width: 100%;
  margin-top: 4px;
}

.disease-error {
  margin-top: 10px;
  color: #c62828;
  font-size: 0.9rem;
  min-height: 1.2em;
}

.disease-result {
  padding: 28px;
  min-height: 320px;
}

.disease-hint {
  color: var(--muted);
  font-size: 0.95rem;
  margin-bottom: 18px;
}

.disease-main-result {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: 16px;
  margin-bottom: 16px;
}

.disease-label {
  font-size: 0.95rem;
  color: var(--muted);
}

.disease-value {
  font-family: "Orbitron", sans-serif;
  font-size: 1.3rem;
  color: var(--primary);
  text-align: right;
}

.disease-advisory-block {
  margin-top: 20px;
  padding: 16px;
  border-radius: 18px;
  background: rgba(124, 179, 66, 0.08);
  border: 1px solid var(--border);
}

.disease-advisory-block h4 {
  margin-bottom: 6px;
  color: var(--text);
}

.disease-advice-text {
  font-size: 0.95rem;
  color: var(--muted);
  line-height: 1.6;
}

.btn--loading {
  opacity: 0.8;
  pointer-events: none;
}

@media (max-width: 900px) {

  .disease-layout {
    grid-template-columns: 1fr;
  }
}


/* ============================================================
   STREAMLIT COMPATIBILITY
   ============================================================ */

.stApp {
  background:
    radial-gradient(
      circle at top left,
      rgba(124, 179, 66, 0.15),
      transparent 28%
    ),
    radial-gradient(
      circle at top right,
      rgba(67, 160, 71, 0.12),
      transparent 28%
    ),
    linear-gradient(
      135deg,
      var(--bg),
      var(--bg2)
    );

  color: var(--text);
}


/* Main content width */

.block-container {
  max-width: 1180px;
  padding-top: 2rem;
  padding-bottom: 4rem;
}


/* ============================================================
   STREAMLIT HEADINGS AND TEXT
   ============================================================ */

.stMarkdown,
.stMarkdown p,
.stMarkdown li {
  color: var(--text);
}

h1,
h2,
h3,
h4,
h5,
h6 {
  color: var(--text) !important;
}

[data-testid="stCaptionContainer"] {
  color: var(--muted) !important;
}

/* Hide Streamlit's default top header */
header[data-testid="stHeader"] {
    display: none !important;
}

/* Remove the space reserved for the header */
.stAppViewContainer {
    padding-top: 0 !important;
}

.main .block-container {
    padding-top: 1rem !important;
}

/* ============================================================
   STREAMLIT LABELS
   ============================================================ */

.stNumberInput label,
.stTextInput label {
  color: var(--text) !important;
}


/* ============================================================
   STREAMLIT INPUT BOXES
   ============================================================ */

.stNumberInput input,
.stTextInput input {
  color: #1b4332 !important;
  -webkit-text-fill-color: #1b4332 !important;
  background: transparent !important;
  caret-color: var(--primary) !important;
}


/* Input container */

div[data-baseweb="input"] {
  background: #ffffff !important;
  border-radius: 999px;
  border: 1px solid var(--border);
}


/* Input focus */

div[data-baseweb="input"]:focus-within {
  border-color: var(--primary) !important;
  box-shadow:
    0 0 0 1px rgba(46, 125, 50, 0.25) !important;
}


/* Number input +/- buttons */

.stNumberInput button {
  color: var(--primary) !important;
}

.stNumberInput button:hover {
  background: rgba(124, 179, 66, 0.12) !important;
}


/* ============================================================
   STREAMLIT BUTTON
   ============================================================ */

.stButton > button {
  width: 100%;
  min-height: 48px;

  border-radius: 999px;

  border: none;

  background:
    linear-gradient(
      135deg,
      var(--primary),
      var(--secondary)
    );

  color: #ffffff !important;

  font-weight: 700;

  transition: 0.3s ease;
}

.stButton > button:hover {
  transform: translateY(-2px);

  box-shadow:
    0 10px 30px
    rgba(46, 125, 50, 0.22);
}


/* ============================================================
   STREAMLIT ALERTS
   ============================================================ */

div[data-testid="stAlert"] {
  border-radius: 18px;
}

div[data-testid="stAlert"] p {
  color: var(--text) !important;
}


/* ============================================================
   STREAMLIT METRIC
   ============================================================ */

div[data-testid="stMetric"] {
  background: rgba(255, 255, 255, 0.80);

  border:
    1px solid
    var(--border);

  border-radius: 18px;

  padding: 18px;
}

div[data-testid="stMetric"] label {
  color: var(--muted) !important;
}

div[data-testid="stMetric"] [data-testid="stMetricValue"] {
  color: var(--primary) !important;
}


/* ============================================================
   DIVIDER
   ============================================================ */

hr {
  border-color: rgba(46, 125, 50, 0.15) !important;
}


/* ============================================================
   MOBILE
   ============================================================ */

@media (max-width: 768px) {

  .stNumberInput input,
  .stTextInput input {
    color: #1b4332 !important;
    -webkit-text-fill-color: #1b4332 !important;
    font-size: 16px !important;
  }

  div[data-baseweb="input"] {
    background: #ffffff !important;
  }

  .block-container {
    padding-left: 1rem;
    padding-right: 1rem;
  }
}


/* ============================================================
   HIDE DEFAULT FOOTER / MENU
   ============================================================ */

footer {
  visibility: hidden;
}

#MainMenu {
  visibility: hidden;
}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# LOAD MODEL
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "models" / "crop_recommendation_model.pkl"
FEATURE_PATH = BASE_DIR / "models" / "feature_columns.pkl"


@st.cache_resource
def load_model():

    model = joblib.load(MODEL_PATH)

    feature_columns = joblib.load(FEATURE_PATH)

    return model, feature_columns


try:

    model, feature_columns = load_model()

except FileNotFoundError:

    st.error(
        "Model files were not found."
    )

    st.info(
        "Please make sure your project contains:\n\n"
        "models/crop_recommendation_model.pkl\n\n"
        "models/feature_columns.pkl"
    )

    st.stop()


# ============================================================
# HERO SECTION
# ============================================================

st.markdown(
    '<div class="hero-bg-grid"></div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="eyebrow">SMART AGRICULTURE • ML RECOMMENDATION</div>',
    unsafe_allow_html=True
)

st.markdown(
    "# Find the right <span style='color:#2e7d32;'>crop</span> for your soil.",
    unsafe_allow_html=True
)

st.markdown(
    """
    Enter the soil nutrient and environmental conditions of your
    field to receive a machine-learning based crop recommendation.
    """
)

# SPACING

st.write("")

# SECTION TITLE

st.markdown("## 🌱 Crop Recommendation")

st.write("")

# TWO COLUMN LAYOUT

input_column, result_column = st.columns(
    [1.1, 0.9],
    gap="large"
)

# INPUT SECTION

with input_column:

    st.subheader("Field Parameters")

    st.caption(
        "Enter the values measured or estimated for your field."
    )

    # ROW 1

    col1, col2 = st.columns(2)

    with col1:

        N = st.number_input(
            "Nitrogen (N)",
            min_value=0.0,
            max_value=200.0,
            value=90.0,
            step=1.0,
            help="Nitrogen content in the soil."
        )

    with col2:

        P = st.number_input(
            "Phosphorus (P)",
            min_value=0.0,
            max_value=150.0,
            value=42.0,
            step=1.0,
            help="Phosphorus content in the soil."
        )

    # ROW 2

    col1, col2 = st.columns(2)

    with col1:

        K = st.number_input(
            "Potassium (K)",
            min_value=0.0,
            max_value=210.0,
            value=43.0,
            step=1.0,
            help="Potassium content in the soil."
        )

    with col2:

        temperature = st.number_input(
            "Temperature (°C)",
            min_value=-10.0,
            max_value=60.0,
            value=25.0,
            step=0.1,
            help="Temperature in degrees Celsius."
        )

    # ROW 3

    col1, col2 = st.columns(2)

    with col1:

        humidity = st.number_input(
            "Humidity (%)",
            min_value=0.0,
            max_value=100.0,
            value=80.0,
            step=0.1,
            help="Relative humidity percentage."
        )

    with col2:

        ph = st.number_input(
            "Soil pH",
            min_value=0.0,
            max_value=14.0,
            value=6.5,
            step=0.1,
            help="Soil pH value."
        )

    # ROW 4

    rainfall = st.number_input(
        "Rainfall (mm)",
        min_value=0.0,
        max_value=500.0,
        value=200.0,
        step=1.0,
        help="Rainfall in millimeters."
    )

    st.write("")

    # PREDICT BUTTON

    predict_button = st.button(
        "Predict Crop 🌱",
        use_container_width=True
    )


# ============================================================
# RESULT SECTION
# ============================================================

with result_column:

    st.subheader("Prediction Result")

    st.caption(
        "Your recommended crop and prediction confidence "
        "will appear here."
    )

    if predict_button:

        # INPUT DATAFRAME

        input_data = pd.DataFrame(
            [{
                "N": N,
                "P": P,
                "K": K,
                "temperature": temperature,
                "humidity": humidity,
                "ph": ph,
                "rainfall": rainfall
            }]
        )

        # ENSURE FEATURE ORDER

        input_data = input_data[feature_columns]

        # PREDICT

        prediction = model.predict(input_data)[0]

        # PROBABILITIES

        probabilities = model.predict_proba(input_data)[0]

        classes = model.classes_

        ranked_predictions = sorted(
            zip(classes, probabilities),
            key=lambda x: x[1],
            reverse=True
        )

        confidence = ranked_predictions[0][1] * 100

        # RECOMMENDED CROP

        st.success(
            f"Recommended Crop: {str(prediction).title()}"
        )

        st.metric(
            "Prediction Confidence",
            f"{confidence:.2f}%"
        )

        st.markdown("### Top 3 Recommendations")

        # TOP 3 CROPS

        for rank, (crop, probability) in enumerate(
            ranked_predictions[:3],
            start=1
        ):

            col_a, col_b = st.columns([3, 1])

            with col_a:

                st.write(
                    f"**{rank}. {str(crop).title()}**"
                )

            with col_b:

                st.write(
                    f"**{probability * 100:.2f}%**"
                )

    else:

        st.info(
            "Enter your field conditions and click "
            "'Predict Crop 🌱' to see the recommendation."
        )


# ============================================================
# HOW IT WORKS
# ============================================================

st.divider()

st.markdown("## How it works")

st.markdown(
    """
    The system analyzes soil and environmental conditions using
    a trained machine-learning classification model.
    """
)

col1, col2, col3 = st.columns(3)

with col1:

    st.markdown("### 🧪 Soil Parameters")

    st.write(
        "Nitrogen, phosphorus, potassium and soil pH "
        "are used to understand the soil conditions."
    )

with col2:

    st.markdown("### 🌦️ Environmental Conditions")

    st.write(
        "Temperature, humidity and rainfall provide "
        "information about the growing environment."
    )

with col3:

    st.markdown("### 🤖 ML Prediction")

    st.write(
        "A trained Random Forest classifier analyzes "
        "the parameters and recommends suitable crops."
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Smart Agriculture Advisory • Powered by Machine Learning 🌱"
)

