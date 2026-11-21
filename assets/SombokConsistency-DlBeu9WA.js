import{e as w,H as U,G as e}from"./vendor-core-CPG7pj0t.js";import{f as X,aW as z,X as T,R as _,U as J,aQ as Q,H as ee,S as $,d as te,M as ae,c as re,aV as se}from"./index-DrNbjXaq.js";import"./vendor-firebase-7nG5f1CA.js";const ie=s=>[{id:"cons_adaptive",category:"consistency",angle:`GEOMETRY-FIRST CONSISTENCY MODE

You are given:

[TARGET IMAGE]
The image that defines the geometry, composition, subject placement, object placement, perspective, scale, and spatial relationships.

[REFERENCE IMAGE]
The image that defines the material appearance, color palette, lighting, atmosphere, realism level, rendering quality, environment, and visual style.

STEP 1 — GEOMETRY ANALYSIS

Before generating the final image, analyze the TARGET IMAGE and identify:
* Primary subject(s)
* Geometry and structure
* Shapes and proportions
* Spatial relationships
* Object locations
* Scale hierarchy
* Camera position
* Camera angle
* Perspective
* Composition
* Visible architectural or environmental elements

Create an internal geometry map and treat it as LOCKED.

STEP 2 — GEOMETRY LOCK

The geometry map from the TARGET IMAGE is the highest priority instruction.
Treat the TARGET IMAGE as a frozen 3D scene.

Do not modify:
* geometry
* proportions
* structure
* layout
* object placement
* subject placement
* camera position
* camera angle
* perspective
* composition

Do not:
* redesign
* reinterpret
* improve
* replace
* invent
* relocate
* remove
* generate new major elements

STEP 3 — APPEARANCE TRANSFER

Transfer from the REFERENCE IMAGE only:
* materials
* textures
* colors
* roughness
* glossiness
* reflections
* transparency
* surface quality
* lighting
* exposure
* atmosphere
* environment
* realism level
* rendering quality

Apply these attributes onto the locked geometry from the TARGET IMAGE.

STEP 4 — FINAL RECONSTRUCTION

Generate a photorealistic image that preserves the TARGET IMAGE exactly while adopting the material appearance, lighting behavior, environment, and visual quality of the REFERENCE IMAGE.

FINAL PRIORITY ORDER:
1. Geometry Fidelity
2. Object Placement Fidelity
3. Camera Fidelity
4. Material Consistency
5. Lighting Consistency
6. Style Consistency

If a conflict occurs, always preserve geometry and composition from the TARGET IMAGE.`,label:"Adaptive Style Match",icon:"M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01",description:"Retains the layout of your new target view, blending them with the ultra-realistic lighting, specific material colors (like wood/stone finishes), and photographic quality of your style reference."},{id:"cons_detail",category:"consistency",angle:`GEOMETRY-FIRST CONSISTENCY MODE (CLOSE-UP DETAIL FOCUS)

You are given:

[TARGET IMAGE]
The image that defines the geometry, composition, subject placement, object placement, perspective, scale, and spatial relationships of the macro subject.

[REFERENCE IMAGE]
The image that defines the material appearance, color palette, lighting, atmosphere, realism level, rendering quality, environment, and visual style.

STEP 1 — GEOMETRY ANALYSIS

Before generating the final image, analyze the TARGET IMAGE and identify:
* Primary subject(s) and key patterns
* Geometry and structure
* Shapes and proportions
* Spatial relationships
* Object locations
* Scale hierarchy
* Camera position
* Camera angle
* Perspective
* Composition

Create an internal geometry map and treat it as LOCKED.

STEP 2 — GEOMETRY LOCK

The geometry map from the TARGET IMAGE is the highest priority instruction.
Treat the TARGET IMAGE as a frozen 3D scene.

Do not modify:
* geometry
* proportions
* structure
* layout
* object placement
* subject placement
* camera position
* camera angle
* perspective
* composition

Do not:
* redesign
* reinterpret
* improve
* replace
* invent
* relocate
* remove
* generate new major elements

STEP 3 — APPEARANCE & DETAIL TRANSFER

Transfer from the REFERENCE IMAGE only:
* materials
* textures
* colors
* roughness
* glossiness
* reflections
* transparency
* surface quality
* lighting
* exposure
* atmosphere
* environment
* realism level
* rendering quality

Apply these attributes onto the locked geometry from the TARGET IMAGE.
CRITICAL DETAIL FOCUS: If the target object has specific zebra stripes, geometric patterns, or text, you MUST keep them perfectly sharp. Apply a cinematic depth of field (shallow focus) to blur the background slightly. Clone the specular highlights and edge-lighting from the style reference.

STEP 4 — FINAL RECONSTRUCTION

Generate a photorealistic image that preserves the TARGET IMAGE exactly while adopting the material appearance, lighting behavior, environment, and visual quality of the REFERENCE IMAGE.

FINAL PRIORITY ORDER:
1. Geometry & Pattern Fidelity
2. Object Placement Fidelity
3. Camera Fidelity
4. Material Consistency
5. Lighting Consistency
6. Style Consistency

If a conflict occurs, always preserve geometry, patterns, and composition from the TARGET IMAGE.`,label:"Close-up Detail",icon:"M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607zM10.5 7.5v6m3-3h-6",description:"Focuses on intricate objects, decor, and furniture textures. Adds professional macro lighting and background blur while strictly keeping figurine patterns intact."}],ne=s=>[{id:"cons_exterior_facade",category:"consistency_exterior",angle:`[EXTERIOR FACADE CONSISTENCY MODE]

[IMAGE ROLES]
Image 1 is the TARGET IMAGE to transform. It is the absolute authority for building geometry, camera, composition, façade layout, site organization, landscaping positions, and all visible objects.
Image 2 is the REFERENCE IMAGE. Use it only for façade finish quality, material appearance, color character, outdoor lighting, sky, atmosphere, landscape realism, and photographic response.
Never copy architecture, camera angle, composition, proportions, openings, or site layout from Image 2.

[PRIMARY TASK]
Transform Image 1 into a photorealistic exterior architectural photograph while preserving its architecture, camera, and spatial organization exactly.
Apply only the visual appearance and photographic qualities of Image 2 to the locked exterior design of Image 1.

[INTERNAL SCENE ANALYSIS & GEOMETRY LOCK]
Before generating, internally identify and map elements from Image 1:
• Building silhouette, overall massing, roofline, parapet profile, and façade proportions
• Window, door, and opening positions, columns, beams, walls, and structural supports
• Overhangs, canopies, balconies, terraces, entrance positions, and circulation routes
• Steps, ramps, platforms, planters, pavements, roads, driveways, landscape boundaries
• Existing trees, vegetation, furniture, vehicles, and site objects
• Camera position, eye height, viewing direction, lens perspective, horizon, vanishing points, crop, and composition
Treat this internal scene map as locked. Do not zoom, rotate, tilt, shift, straighten, widen, compress, recrop, or create a new viewpoint.

[SITE AND OBJECT LOCK]
Preserve the complete site layout shown in Image 1:
• Roads, driveways, parking areas, paths, pavements, curbs, steps, drainage lines, planters, planting beds
• Trees, shrubs, lawns, exterior furniture, lighting fixtures, signs, vehicles, and neighboring structures
Maintain exact positions, dimensions, quantities, boundaries, orientation, and relationship to the building.
Improve realism without relocating, replacing, enlarging, removing, or inventing elements.

[REFERENCE APPEARANCE TRANSFER]
Transfer from Image 2 only:
• Façade material appearance, finish quality, stone, concrete, plaster, brick, timber, glass, and metal characteristics
• Surface texture, scale, roughness, reflectivity, weathering, glass clarity, tint, and reflection behavior
• General color palette, exterior ground finish quality, landscaping character, and botanical realism
• Outdoor lighting quality, color temperature, sun direction, shadow softness, time-of-day atmosphere, sky color, cloud character, haze, and photographic color response
Apply these qualities only to corresponding regions already present in Image 1.

[MATERIAL & LIGHTING RULES]
• Reference wall finishes apply only to walls; reference glazing applies only to existing glass; reference paving applies only to corresponding ground surfaces
• Do not allow textures or materials to cross windows, joints, corners, trims, openings, structural edges, or ground boundaries
• Match lighting and atmospheric character of Image 2 while keeping Image 1’s architecture and site unchanged
• Preserve physically plausible illumination, natural shadow direction, realistic contact shadows, balanced exposure, accurate reflections, and believable interior-to-exterior light levels
• Activate only lighting fixtures already visible or indicated in Image 1

[PHOTOREALISM ENHANCEMENT & FINAL OUTPUT]
• Replace flat or synthetic appearance with realistic micro-texture, subtle material imperfections, accurate reflections, glass behavior, and ambient occlusion
• All realism enhancements must remain inside existing geometry and material boundaries
• Generate a convincing real-world DSLR exterior architectural photograph that preserves Image 1’s exact building, camera, composition, site layout, and object positions while adopting Image 2’s material finish quality, lighting, sky, atmosphere, and photographic response
• Must look photographed on location—not like a CGI render

[PRIORITY ORDER]
1. Camera, perspective, crop, and composition fidelity
2. Building silhouette, massing, and geometry fidelity
3. Window, door, entrance, and structural-position fidelity
4. Site layout, landscaping, and object-position fidelity
5. Correct material placement and boundary control
6. Reference lighting, sky, and atmospheric consistency
7. Photographic realism and finish quality

If any instruction conflicts, always preserve camera, architecture, site layout, and spatial relationships from Image 1.`,label:"Exterior Facade Match",icon:"M8.25 21v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21m0 0h4.5V3.545M12.75 21h7.5V10.75M2.25 21h1.5m18 0h-18M2.25 9l4.5-1.636M18.75 3l-1.5.545m0 6.205l3 1m1.5.5l-1.5-.5M6.75 7.364V3h-3v18m3-13.636l10.5-3.819",description:"Preserves the exact building silhouette, roofline, and facade proportions from your target while transferring exterior cladding, glass finishes, outdoor lighting, sky conditions, and environmental context from your style reference."}],q=({title:s,subtitle:r,icon:d,color:i,isExpanded:u,onToggle:p})=>e.jsxs("div",{className:"flex items-center justify-between w-full group/header",children:[e.jsxs("div",{className:"flex items-center gap-6",children:[e.jsx("div",{onClick:p,className:`p-3 rounded-2xl bg-${i}-500/10 border border-${i}-500/20 text-${i}-400 shadow-glow-sm shadow-${i}-500/10 cursor-pointer hover:bg-${i}-500/20 transition-all active:scale-95`,children:d}),e.jsxs("div",{className:"cursor-pointer",onClick:p,children:[e.jsx("h4",{className:"text-xl font-black text-white uppercase tracking-tight",children:s}),r?e.jsx("p",{className:"text-[10px] text-text-secondary font-black uppercase tracking-[0.2em] mt-1.5 opacity-60 leading-none",children:r}):e.jsx("div",{className:`h-1 w-12 bg-${i}-500/40 rounded-full mt-2`})]})]}),e.jsxs("div",{className:"flex items-center gap-6 ml-auto",children:[e.jsx("div",{className:"hidden lg:block h-px w-32 bg-white/5"}),e.jsxs("button",{onClick:p,className:"group/toggle relative flex items-center transition-all duration-300 active:scale-90",children:[e.jsx("div",{className:`w-14 h-7 rounded-full transition-all duration-500 border ${u?`bg-${i}-500/20 border-${i}-500/40 shadow-glow-sm shadow-${i}-400/20`:"bg-white/5 border-white/10"}`}),e.jsx("div",{className:`absolute top-1 left-1.5 w-5 h-5 rounded-full transition-all duration-500 transform ${u?`translate-x-6 bg-${i}-400 shadow-glow-sm shadow-${i}-400/50`:"translate-x-0 bg-white/20"}`})]})]})]}),oe=({image:s,color:r,title:d,description:i,badge:u,onUpload:p,onDelete:g})=>e.jsxs("div",{className:"group/base relative bg-bg-secondary/40 border border-white/5 rounded-[32px] overflow-hidden transition-all duration-500 hover:bg-bg-secondary/60 hover:border-white/10 flex flex-col h-full ring-1 ring-white/5 ring-inset",children:[e.jsxs("div",{className:"relative w-full aspect-video overflow-hidden bg-bg-tertiary/20",children:[e.jsx("img",{src:s,className:"w-full h-full object-cover transition-transform duration-700 group-hover/base:scale-105",alt:"Base Image"}),e.jsxs("div",{className:"absolute inset-0 bg-black/50 opacity-0 group-hover/base:opacity-100 transition-opacity flex items-center justify-center gap-4 z-20",children:[p&&e.jsx("button",{onClick:x=>{x.stopPropagation(),p()},className:"p-3 bg-white/10 hover:bg-brand-primary rounded-xl backdrop-blur-md text-white transition-all transform hover:scale-110",children:e.jsx(_,{className:"w-5 h-5"})}),g&&e.jsx("button",{onClick:x=>{x.stopPropagation(),g()},className:"p-3 bg-red-500/20 hover:bg-red-500 rounded-xl backdrop-blur-md text-white transition-all transform hover:scale-110",children:e.jsx(T,{className:"w-5 h-5"})})]}),e.jsxs("div",{className:"absolute top-4 left-4 px-3 py-1.5 bg-black/40 backdrop-blur-md rounded-xl border border-white/10 flex items-center gap-2",children:[e.jsx("div",{className:`w-1.5 h-1.5 rounded-full bg-${r}-400 animate-pulse`}),e.jsx("span",{className:"text-[9px] font-black uppercase tracking-widest text-white",children:u})]})]}),e.jsx("div",{className:"w-full p-6 flex flex-col gap-4 flex-grow justify-center relative",children:e.jsxs("div",{children:[e.jsx("h5",{className:`text-[11px] font-black text-white uppercase tracking-widest mb-1 group-hover/base:text-${r}-400 transition-colors`,children:d}),e.jsx("p",{className:"text-[9px] text-text-secondary leading-relaxed font-medium",children:i})]})})]}),Y=({config:s,result:r,isLoading:d,onGenerate:i,onZoom:u,unitCost:p,customPrompt:g,onPromptChange:x,targetImage:l,selectedModel:j,t:f})=>e.jsxs("div",{className:"group/card relative bg-bg-secondary/40 border border-white/5 rounded-[32px] overflow-hidden transition-all duration-500 hover:bg-bg-secondary/60 hover:border-white/10 hover:shadow-2xl flex flex-col md:flex-row w-full col-span-full",children:[e.jsx("style",{dangerouslySetInnerHTML:{__html:`
      @keyframes sweep {
        0% { top: 0%; }
        50% { top: 100%; }
        100% { top: 0%; }
      }
      @keyframes spin-slow-cw {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
      }
      @keyframes spin-slow-ccw {
        from { transform: rotate(0deg); }
        to { transform: rotate(-360deg); }
      }
      @keyframes text-pulse {
        0%, 100% { opacity: 0.4; }
        50% { opacity: 1; }
      }
    `}}),e.jsxs("div",{className:"relative w-full md:w-1/2 aspect-video overflow-hidden bg-bg-tertiary/20 shrink-0 border border-white/5 rounded-2xl",children:[d?e.jsxs("div",{className:"relative w-full h-full flex flex-col items-center justify-center bg-black/45 overflow-hidden",children:[e.jsx("img",{src:l,className:"absolute inset-0 w-full h-full object-cover filter blur-[6px] grayscale-[50%] brightness-[0.35] scale-105",alt:"Rendering Background"}),e.jsx("div",{className:"absolute w-32 h-32 bg-brand-primary/10 rounded-full blur-2xl animate-pulse"}),e.jsx("div",{className:"absolute w-40 h-40 bg-purple-500/5 rounded-full blur-3xl animate-pulse",style:{animationDelay:"1s"}}),e.jsx("div",{className:"absolute left-0 right-0 h-[2px] bg-gradient-to-r from-transparent via-brand-primary/80 to-transparent shadow-[0_0_15px_rgba(45,212,191,0.8)] z-10",style:{animation:"sweep 4s infinite ease-in-out"}}),e.jsxs("div",{className:"relative w-24 h-24 flex items-center justify-center z-10",children:[e.jsx("div",{className:"absolute inset-0 rounded-full border border-dashed border-brand-primary/30",style:{animation:"spin-slow-cw 8s linear infinite"}}),e.jsx("div",{className:"absolute inset-2 rounded-full border border-dotted border-purple-400/40",style:{animation:"spin-slow-ccw 6s linear infinite"}}),e.jsx("div",{className:"absolute inset-4 bg-gradient-to-br from-brand-primary/10 to-purple-500/10 rounded-full border border-white/10 flex items-center justify-center backdrop-blur-sm shadow-inner",children:e.jsx($,{className:"w-6 h-6 text-brand-primary animate-spin"})})]}),e.jsxs("div",{className:"mt-4 flex flex-col items-center gap-1 z-10",children:[e.jsx("span",{className:"text-[10px] font-black uppercase tracking-[0.25em] text-brand-primary drop-shadow-[0_0_8px_rgba(45,212,191,0.5)] animate-pulse",children:"Rendering..."}),e.jsx("span",{className:"text-[7px] font-medium uppercase tracking-[0.2em] text-white/40 animate-pulse",style:{animationDuration:"2s"},children:"AI consistency engine active"})]})]}):r?e.jsx("img",{src:r.imageData,className:"w-full h-full object-cover transition-transform duration-700 group-hover/card:scale-105",alt:s.label}):e.jsxs("div",{className:"relative w-full h-full flex items-center justify-center bg-black/35 overflow-hidden",children:[e.jsx("img",{src:l,className:"absolute inset-0 w-full h-full object-cover filter grayscale-[90%] brightness-[0.2] contrast-[0.8] transition-transform duration-700 group-hover/card:scale-105",alt:"Ready Background"}),e.jsx("div",{className:"absolute inset-0 opacity-[0.03] pointer-events-none",style:{backgroundImage:"radial-gradient(circle at 2px 2px, white 1px, transparent 0)",backgroundSize:"16px 16px"}}),e.jsxs("div",{className:"relative flex flex-col items-center gap-3.5 z-10",children:[e.jsx("div",{className:"p-3 bg-white/[0.02] border border-white/5 rounded-2xl group-hover/card:border-brand-primary/30 group-hover/card:bg-brand-primary/5 transition-all duration-500 shadow-xl",children:e.jsx(te,{className:"w-8 h-8 text-white/20 group-hover/card:text-brand-primary/70 transition-colors duration-500 animate-pulse"})}),e.jsxs("div",{className:"flex flex-col items-center gap-1",children:[e.jsx("span",{className:"text-[8px] font-black uppercase tracking-[0.25em] text-white/30 group-hover/card:text-white/60 transition-colors duration-500",children:"Ready to Render"}),e.jsx("div",{className:"w-4 h-[1px] bg-white/10 group-hover/card:w-8 group-hover/card:bg-brand-primary/30 transition-all duration-500"})]})]})]}),r&&!d&&e.jsxs("div",{className:"absolute top-4 right-4 flex gap-2 opacity-0 group-hover/card:opacity-100 transition-opacity z-20",children:[e.jsx("button",{onClick:()=>u(r.imageData),className:"p-2.5 bg-black/40 hover:bg-brand-primary backdrop-blur-xl rounded-xl text-white transition-all transform hover:scale-110 border border-white/10",children:e.jsx(ae,{className:"w-4 h-4"})}),e.jsx("button",{onClick:()=>{const c=document.createElement("a");c.href=r.imageData,c.download=`consistency-${s.id}.png`,c.click()},className:"p-2.5 bg-black/40 hover:bg-brand-primary backdrop-blur-xl rounded-xl text-white transition-all transform hover:scale-110 border border-white/10",children:e.jsx(re,{className:"w-4 h-4"})})]})]}),e.jsxs("div",{className:"w-full md:w-1/2 p-6 md:p-8 flex flex-col justify-center gap-4 flex-grow",children:[e.jsxs("div",{children:[e.jsx("h5",{className:"text-xl font-black text-white uppercase tracking-widest mb-3 group-hover/card:text-brand-primary transition-colors",children:s.label}),e.jsx("p",{className:"text-xs text-text-secondary leading-relaxed font-medium",children:s.description||"Automated style and object synchronization across spatial perspectives."})]}),e.jsxs("div",{className:"mt-2 space-y-2",children:[e.jsx("div",{className:"flex items-center justify-between ml-1",children:e.jsx("label",{className:"text-[9px] font-black text-white/40 uppercase tracking-widest",children:"Custom Extra Instructions (Optional)"})}),e.jsx("textarea",{value:g||"",onChange:c=>x(c.target.value),placeholder:"e.g. Use dark walnut wood, add more plants, natural morning sun...",className:"w-full h-20 bg-black/20 border border-white/5 rounded-2xl p-4 text-[11px] text-white placeholder:text-white/20 focus:border-brand-primary/50 focus:ring-1 focus:ring-brand-primary/20 transition-all resize-none outline-none"})]}),e.jsx("div",{className:"mt-2",children:e.jsxs("button",{onClick:()=>i(s.angle,s.id,s.label),disabled:d,className:`w-full md:w-auto px-10 py-4 rounded-2xl text-[11px] font-black uppercase tracking-widest transition-all flex items-center justify-center gap-3 border shadow-xl ${r?"bg-white/5 border-white/10 text-white hover:bg-white/10":"bg-brand-primary border-brand-primary text-white shadow-glow-sm shadow-brand-primary/20 hover:scale-[1.02]"} disabled:opacity-20 disabled:cursor-not-allowed`,children:[d?e.jsx($,{className:"w-5 h-5 animate-spin"}):e.jsx(se,{model:j,className:"w-5 h-5"}),d?f("generating")||"GENERATING":`${r?f("regenerate")||"REGENERATE":f("generate")||"GENERATE"} (${p})`]})})]})]}),pe=({state:s,actions:r,galleryResolution:d="1K",galleryAspectRatio:i})=>{const{isSombokConsistencyEnabled:u,renovationSourceImage:p,activeEnhancedImage:g,galleryHistory:x,originalImage:l,isLoading:j,t:f}=s,[c,k]=w.useState(null),[N,A]=w.useState(null),[I,S]=w.useState({}),[M,G]=w.useState({}),[y,E]=w.useState(null),C=U.useRef(null),O=U.useRef(null),[R,B]=w.useState({consistency:!0,exterior:!0}),P=t=>{B(a=>({...a,[t]:!a[t]}))};if(!u)return null;const v=(N==null?void 0:N.data)||p||(g===(l==null?void 0:l.data)?l==null?void 0:l.data:null)||g||(l==null?void 0:l.data);if(!v)return null;const H=ie(),V=ne(),K=t=>{var n;const a=(n=t.target.files)==null?void 0:n[0];if(a){const o=new FileReader;o.onload=m=>{var h;if((h=m.target)!=null&&h.result){const b=m.target.result;E({data:b,file:a,type:"style"})}},o.readAsDataURL(a)}},W=async t=>{if(!y)return;const a=y.type,n=o=>{var m;a==="style"?(k(o),(m=r.setDesignReferences)==null||m.call(r,h=>({...h,style_reference:o}))):a==="target"&&A(o),E(null)};r.applyCropToFile?await r.applyCropToFile(y,t,n):n(y)},Z=t=>{var n;const a=(n=t.target.files)==null?void 0:n[0];if(a){const o=new FileReader;o.onload=m=>{var h;if((h=m.target)!=null&&h.result){const b=m.target.result;E({data:b,file:a,type:"target"})}},o.readAsDataURL(a)}},F=async(t,a,n)=>{var h;if(!c){(h=r.setError)==null||h.call(r,"Please upload an AI generated or standard image to extract Consistency parameters.");return}const o=I[a],m=o?`${t} CUSTOM OVERRIDE: ${o}.`:t;G(b=>({...b,[a]:!0}));try{await r.handleGenerateAngle(m,a,n,v)}finally{G(b=>({...b,[a]:!1}))}},D=t=>[...x].reverse().find(a=>a.originalImageData===v&&(a.prompt.includes(t.angle)||a.prompt.includes(`NEURAL PERSPECTIVE SHIFT: ${t.angle}`))),L=()=>r.getGalleryUnitCost();return e.jsxs(e.Fragment,{children:[y&&e.jsx(X,{imageSrc:y.data,onCrop:W,onCancel:()=>E(null),t:f}),e.jsxs("div",{"data-feature-panel":"consistency",className:"bg-glass-heavy backdrop-blur-3xl border border-white/10 rounded-[40px] p-6 lg:p-12 shadow-2xl animate-fadeInUp relative overflow-hidden my-12 group/consistency",children:[e.jsx("div",{className:"absolute -top-24 -right-24 w-96 h-96 bg-brand-primary/10 rounded-full blur-[120px] pointer-events-none group-hover/consistency:bg-brand-primary/15 transition-colors duration-700"}),e.jsx("div",{className:"absolute -bottom-24 -left-24 w-96 h-96 bg-purple-500/5 rounded-full blur-[120px] pointer-events-none"}),e.jsxs("div",{className:"flex flex-col md:flex-row items-center justify-between gap-8 mb-12 relative",children:[e.jsxs("div",{className:"flex items-center gap-6",children:[e.jsxs("div",{className:"relative",children:[e.jsx("div",{className:"absolute inset-0 bg-brand-primary/20 blur-xl rounded-full scale-75 animate-pulse"}),e.jsx("div",{className:"relative p-4 bg-gradient-to-br from-brand-primary/20 to-indigo-500/20 rounded-2xl border border-brand-primary/30 shadow-glow-sm shadow-brand-primary/10",children:e.jsx(z,{className:"w-7 h-7 text-brand-primary"})})]}),e.jsxs("div",{children:[e.jsxs("div",{className:"flex items-center gap-4",children:[e.jsx("h3",{className:"text-2xl font-black text-text-primary uppercase tracking-tight flex items-center gap-2",children:"Consistency"}),e.jsxs("div",{className:"flex items-center gap-2 px-3 py-1 bg-purple-500/10 rounded-full border border-purple-500/20",children:[e.jsx("div",{className:"w-1.5 h-1.5 rounded-full bg-purple-500 animate-pulse"}),e.jsx("span",{className:"text-[10px] font-black text-purple-400 uppercase tracking-widest leading-none",children:"A.I Tool"})]})]}),e.jsx("p",{className:"text-[11px] text-text-secondary uppercase tracking-[0.3em] font-black opacity-60 mt-1.5",children:"Synchronize Decor and Lighting across Views"})]})]}),e.jsx("div",{className:"flex items-center gap-4",children:e.jsx("button",{onClick:()=>r.setIsSombokConsistencyEnabled(!1),className:"p-3 bg-white/5 hover:bg-white/10 hover:rotate-90 rounded-2xl border border-white/5 transition-all duration-300 group/close shrink-0 outline-none focus:outline-none focus-visible:outline-none focus:ring-0 active:outline-none select-none active:scale-95",title:"Close Consistency",children:e.jsx(T,{className:"w-5 h-5 text-text-secondary group-hover/close:text-red-400 transition-colors"})})})]}),e.jsxs("div",{className:"flex flex-col gap-16 relative",children:[e.jsxs("div",{className:"space-y-8 animate-fadeInUp",children:[e.jsx(q,{title:"Interior Consistency",subtitle:"Multi-Angle Style Reference",icon:e.jsx(z,{className:"w-5 h-5 flex-shrink-0"}),color:"purple",isExpanded:R.consistency,onToggle:()=>P("consistency")}),R.consistency&&e.jsxs("div",{className:"space-y-8 animate-fadeIn",children:[e.jsxs("div",{className:"grid grid-cols-1 md:grid-cols-2 gap-8",children:[e.jsx(oe,{image:v,color:"purple",title:"Current Perspective",description:"The layout geometry from a new viewpoint.",badge:"Target Context",onUpload:()=>{var t;return(t=O.current)==null?void 0:t.click()},onDelete:N?()=>A(null):void 0}),e.jsx("input",{type:"file",accept:"image/*",className:"hidden",ref:O,onChange:Z}),e.jsxs("div",{className:"group/ref relative bg-bg-secondary/40 border border-white/5 rounded-[32px] overflow-hidden transition-all duration-500 hover:bg-bg-secondary/60 hover:border-white/10 flex flex-col h-full",children:[e.jsxs("div",{className:`relative w-full aspect-video overflow-hidden flex flex-col items-center justify-center bg-bg-tertiary/20 cursor-pointer ${c?"":"hover:bg-white/[0.05]"}`,onClick:()=>{var t;c||(t=C.current)==null||t.click()},children:[c?e.jsxs(e.Fragment,{children:[e.jsx("img",{src:c.data,className:"w-full h-full object-cover transition-transform duration-700 group-hover/ref:scale-105",alt:"Style Reference"}),e.jsxs("div",{className:"absolute inset-0 bg-black/50 opacity-0 group-hover/ref:opacity-100 transition-opacity flex items-center justify-center gap-4 z-20",children:[e.jsx("button",{onClick:t=>{var a;t.stopPropagation(),(a=C.current)==null||a.click()},className:"p-3 bg-white/10 hover:bg-brand-primary rounded-xl backdrop-blur-md text-white transition-all transform hover:scale-110",children:e.jsx(_,{className:"w-5 h-5"})}),e.jsx("button",{onClick:t=>{var a;t.stopPropagation(),k(null),(a=r.setDesignReferences)==null||a.call(r,n=>{const o={...n};return delete o.style_reference,o})},className:"p-3 bg-red-500/20 hover:bg-red-500 rounded-xl backdrop-blur-md text-white transition-all transform hover:scale-110",children:e.jsx(T,{className:"w-5 h-5"})})]})]}):e.jsxs("div",{className:"w-full h-full flex flex-col items-center justify-center gap-3",children:[e.jsx("div",{className:"p-3 bg-white/[0.03] rounded-xl border border-white/5 group-hover/ref:border-indigo-400/30 transition-colors",children:e.jsx(J,{className:"w-6 h-6 text-purple-400 opacity-60 group-hover/ref:opacity-100 transition-all"})}),e.jsx("span",{className:"text-[10px] uppercase font-black tracking-widest text-white/40 group-hover/ref:text-purple-400 transition-colors",children:"Upload Primary Photo"})]}),e.jsx("input",{type:"file",accept:"image/*",className:"hidden",ref:C,onChange:K}),e.jsxs("div",{className:"absolute top-4 left-4 px-3 py-1.5 bg-black/40 backdrop-blur-md rounded-xl border border-white/10 flex items-center gap-2",children:[e.jsx(Q,{className:"w-3.5 h-3.5 text-purple-400"}),e.jsx("span",{className:"text-[9px] font-black uppercase tracking-widest text-white",children:"Reference"})]})]}),e.jsx("div",{className:"w-full p-6 flex flex-col gap-4 flex-grow justify-center relative",children:e.jsxs("div",{children:[e.jsx("h5",{className:"text-[11px] font-black text-white uppercase tracking-widest mb-1 group-hover/ref:text-purple-400 transition-colors",children:"Style & Decor Origin Master"}),e.jsx("p",{className:"text-[9px] text-text-secondary leading-relaxed font-medium",children:'Upload the "gold standard" render of your space. All angles will inherit details from this shot.'})]})})]})]}),e.jsx("div",{className:"grid grid-cols-1 md:grid-cols-2 gap-6 mt-6",children:H.map(t=>e.jsx(Y,{config:t,result:D(t),isLoading:M[t.id]||j,onGenerate:F,onZoom:r.handleOpenZoom,unitCost:L(),customPrompt:I[t.id],onPromptChange:a=>S(n=>({...n,[t.id]:a})),targetImage:v,selectedModel:s.selectedModel,t:f},t.id))})]})]}),e.jsxs("div",{className:"space-y-8 animate-fadeInUp",style:{animationDelay:"0.1s"},children:[e.jsx(q,{title:e.jsxs("span",{className:"flex items-center gap-2",children:["Exterior Consistency",e.jsxs("span",{className:"relative inline-block",children:[e.jsx("span",{className:"absolute -inset-1 bg-gradient-to-r from-amber-500 to-orange-500 blur opacity-50 animate-pulse"}),e.jsx("span",{className:"relative text-transparent bg-clip-text bg-gradient-to-r from-amber-400 to-orange-400 drop-shadow-[0_0_10px_rgba(245,158,11,0.8)]",children:"NEW"})]})]}),subtitle:"Facade & Landscape Style Transfer",icon:e.jsx(ee,{className:"w-5 h-5 flex-shrink-0"}),color:"amber",isExpanded:R.exterior,onToggle:()=>P("exterior")}),R.exterior&&e.jsx("div",{className:"space-y-8 animate-fadeIn",children:e.jsx("div",{className:"grid grid-cols-1 md:grid-cols-2 gap-6",children:V.map(t=>e.jsx(Y,{config:t,result:D(t),isLoading:M[t.id]||j,onGenerate:F,onZoom:r.handleOpenZoom,unitCost:L(),customPrompt:I[t.id],onPromptChange:a=>S(n=>({...n,[t.id]:a})),targetImage:v,selectedModel:s.selectedModel,t:f},t.id))})})]})]})]})]})};export{pe as SombokConsistency};
