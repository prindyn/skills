# Tool selection for 3D in React

This is the long-form version of the table in SKILL.md. Read when the user is choosing between options or asking "should I use X or Y".

## React Three Fiber (R3F) — default choice

R3F is a React renderer for Three.js. It exposes Three.js classes as JSX components and reuses Three's full feature set. Crucially, it integrates with React's reconciler so mounting/unmounting components correctly disposes Three.js resources (geometries, materials, textures, render targets). This automatic cleanup is the single biggest reason to prefer it over vanilla Three.js inside React.

Pair with **drei** (`@react-three/drei`) — a community helpers library that ships ready-to-use components: `OrbitControls`, `PresentationControls`, `useGLTF`, `useAnimations`, `Environment`, `ContactShadows`, `Text3D`, `Float`, `Sparkles`, `MeshTransmissionMaterial`, `shaderMaterial` factory, scroll utilities, and many more. Roughly 80% of "how do I do X in R3F" answers are "drei has a component for that".

**Pick R3F when:** you're working in any modern React app and need 3D content. This is the default and should be the answer unless the user has specific reasons otherwise.

## Vanilla Three.js (inside React)

Possible but discouraged. Without R3F's reconciler integration, you must manually manage object lifetimes. Every component re-render that creates new Three.js instances without disposing the old ones leaks memory — invisible meshes, shaders, and textures accumulate on the GPU. Crashes don't appear immediately; they appear after the user has navigated around for a few minutes.

**Only pick this when:** you're integrating an existing imperative Three.js codebase (e.g. a designer's published scene), porting from a non-React app, or hitting a specific R3F limitation. Always lift the scene/renderer creation into a `useEffect(() => { ... return cleanup }, [])` and never re-instantiate on re-render.

## Spline (`@splinetool/react-spline`)

Spline is a visual 3D editor. Designers build a scene in the Spline app, export it as a hosted scene URL, and developers drop it into a React component. Animations, hover/click states, and physics are configured in the editor — almost no code on the React side.

```jsx
import Spline from '@splinetool/react-spline'

export function Hero() {
  return <Spline scene="https://prod.spline.design/your-scene-id/scene.splinecode" />
}
```

To trigger Spline events from React or read state out, use the `onLoad` callback to grab the `splineApp` instance, then call `splineApp.emitEvent('mouseDown', 'ObjectName')` or `splineApp.findObjectByName('Cube')`.

**Pick Spline when:** a designer is leading the work, the scene is mostly static or has self-contained interactions, or rapid visual iteration matters more than fine-grained code control. Common fits: marketing hero sections, landing-page decorations, interactive product showcases.

**Trade-offs:** less React-native than R3F (the scene is essentially a black box), bundle size includes Spline's runtime, scenes are typically loaded over the network.

## Babylon.js

Full game engine — comprehensive PBR materials, native physics, WebXR, node-based material editor, animation graph. More opinionated and heavier than Three.js. Per Johansson (2021), consumes ~46% more memory than Three.js for comparable scenes.

No first-class React renderer comparable to R3F. There's `react-babylonjs` but it's smaller and less mature. Most React + Babylon integrations use a `useRef` + `useEffect` pattern to host the engine in a canvas.

**Pick Babylon.js when:** you need WebXR (VR/AR), advanced built-in physics (Havok), or you're explicitly building a web game and want engine-level features. Otherwise R3F covers the ground at lower cost.

## P5.js

A creative-coding library oriented toward 2D and generative art. Has WebGL mode for 3D but isn't really a 3D engine — no scene graph, materials are limited, no built-in model loading.

P5.js manages its own draw loop and DOM, which conflicts with React's reconciliation. Integrating it requires creating a `p5` instance in a `useEffect` and treating its canvas as an opaque box.

**Pick P5.js when:** the brief is generative art, 2D animation with optional 3D primitives, educational sketches, or shader experiments where the user explicitly wants P5's API. **Avoid for** typical "3D model in a React UI" requests — R3F is a better fit.

## When the answer is "don't use 3D at all"

Sometimes the request is decorative motion that doesn't need a 3D scene at all:

- Simple rotating logo or icon → CSS `animation: spin` or `framer-motion` 2D.
- Parallax scrolling cards → `framer-motion` with `useScroll`.
- 2D vector animations with depth illusion → Lottie or `framer-motion`.

If the user asked for a "3D effect" but really wants CSS-level visual flair, point that out and offer the lighter-weight option. Adding R3F to a project pulls in three.js (~600KB gzipped) — worth it for real 3D, overkill for a tilt effect.
