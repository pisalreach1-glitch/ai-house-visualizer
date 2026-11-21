import{G as e}from"./vendor-core-CPG7pj0t.js";const t=()=>e.jsxs("div",{className:"fixed inset-0 z-0 overflow-hidden pointer-events-none bg-bg-primary",children:[e.jsxs("div",{className:"absolute top-0 left-0 right-0 h-full",children:[e.jsx("div",{className:"absolute top-[-10%] left-[10%] w-[320px] h-[320px] md:w-[1000px] md:h-[1000px] bg-brand-primary/40 rounded-full blur-[35px] md:blur-[80px]",style:{animation:"fluid-move-1 22s infinite alternate ease-in-out",opacity:.5,willChange:"transform"}}),e.jsx("div",{className:"absolute top-[-5%] right-[5%] w-[280px] h-[280px] md:w-[800px] md:h-[800px] bg-brand-primary/30 rounded-full blur-[30px] md:blur-[60px]",style:{animation:"fluid-move-2 18s infinite alternate-reverse ease-in-out",mixBlendMode:"screen",opacity:.4,willChange:"transform"}}),e.jsx("div",{className:"absolute top-[10%] left-[30%] w-[340px] h-[340px] md:w-[1100px] md:h-[1100px] bg-purple-600/30 rounded-full blur-[40px] md:blur-[100px]",style:{animation:"fluid-move-3 28s infinite alternate ease-in-out",mixBlendMode:"screen",opacity:.4,willChange:"transform"}})]}),e.jsx("div",{className:"absolute inset-0",style:{backgroundImage:"radial-gradient(circle, #ffffff 1px, transparent 1px)",backgroundSize:"40px 40px",opacity:.15,maskImage:"linear-gradient(to bottom, black 10%, transparent 40%)",WebkitMaskImage:"linear-gradient(to bottom, black 10%, transparent 40%)"}}),e.jsx("div",{className:"absolute inset-0 bg-gradient-to-b from-transparent via-black/40 to-black pointer-events-none"}),e.jsx("style",{children:`
        @media (max-width: 768px) {
          /* Pause continuous GPU re-blur passes on mobile */
          div[style*="fluid-move"] {
            animation: none !important;
          }
        }
        @media (min-width: 769px) {
          @keyframes fluid-move-1 {
            0% { transform: translate(-10%, -10%) rotate(0deg) scale(1); }
            50% { transform: translate(15%, 15%) rotate(15deg) scale(1.1); }
            100% { transform: translate(-5%, 10%) rotate(-5deg) scale(0.9); }
          }
          @keyframes fluid-move-2 {
            0% { transform: translate(10%, 10%) scale(1.1) rotate(0deg); }
            50% { transform: translate(-20%, -15%) scale(1) rotate(-10deg); }
            100% { transform: translate(15%, 10%) scale(1.3) rotate(5deg); }
          }
          @keyframes fluid-move-3 {
            0% { transform: translate(-15%, 15%) scale(0.8); }
            50% { transform: translate(20%, -10%) scale(1.2); }
            100% { transform: translate(-10%, 20%) scale(1); }
          }
        }
      `})]});export{t as ModernBackground};
