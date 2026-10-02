/* Demo / simulated data only. Not real measurements. */
window.SN_DATA = {
  limits: { // CPCB / MoEFCC Noise Pollution (Regulation and Control) Rules, 2000 - dB(A) Leq
    residential: { name: "Residential", day: 55, night: 45 },
    commercial:  { name: "Commercial",  day: 65, night: 55 },
    industrial:  { name: "Industrial",  day: 75, night: 70 },
    silence:     { name: "Silence Zone", day: 50, night: 40 }
  },
  demoBase: { residential: 52, commercial: 62, industrial: 72, silence: 47 },
  zones: [
    { icon: "🏠", name: "Residential", v: 52 }, { icon: "🏥", name: "Hospital", v: 46 },
    { icon: "🏫", name: "School", v: 49 }, { icon: "🚦", name: "Traffic Junction", v: 78 },
    { icon: "🏪", name: "Commercial Market", v: 68 }, { icon: "🏭", name: "Industrial Area", v: 74 }
  ],
  tips: {
    residential: ["Reduce unnecessary vehicle horns.", "Avoid excessive amplified sound.", "Pay attention to nighttime noise."],
    commercial: ["Manage amplified sound.", "Control generator and machinery noise.", "Improve traffic management."],
    industrial: ["Maintain machinery regularly.", "Use acoustic barriers where appropriate.", "Follow environmental noise-control practices."],
    silence: ["Minimize unnecessary horns.", "Restrict excessive amplified sound.", "Give special attention to hospitals, schools and other sensitive locations."]
  }
};
