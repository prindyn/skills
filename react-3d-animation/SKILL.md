---
name: react-3d-animation
description: Build interactive 3D animations inside React applications using React Three Fiber (R3F), drei, and react-spring/three. Use this skill whenever the user wants to add a 3D scene, animated 3D model, rotating/floating object, GLTF/GLB viewer, custom shader effect, hero 3D animation, scroll-driven 3D, or any WebGL/Three.js content into a React app — even if they don't explicitly say "Three.js" or "R3F" (e.g. "spinning logo in React", "3D background", "animated sphere with shaders", "load my .glb file", "make this product card 3D"). Also covers tool selection between R3F, vanilla Three.js, Spline, and Babylon.js for React projects.
---

# React 3D Animation

Help users add and animate 3D content inside React applications. Default to **React Three Fiber (R3F)** unless there's a concrete reason not to — it's the only major option that integrates cleanly with React's lifecycle.

## When this skill applies

Trigger on any of:

- "3D" + "React" / Next.js / Vite / Remix
- Animated 3D scenes, rotating objects, floating cards, hero 3D, scroll-driven 3D
- Loading `.glb`, `.gltf`, `.fbx`, `.obj` in React
- Custom GLSL shaders inside React (vertex/fragment, noise, displacement)
- Spline scenes embedded in React
- "WebGL effect", "Three.js in React", "react-three-fiber", "drei", "react-spring/three"
- Camera animations, OrbitControls, post-processing in React

## Tool selection

Pick one before writing code. The wrong choice leads to memory leaks, jank, or a rewrite.

| User context | Pick | Why |
|---|---|---|
| Anything 3D inside a React app, default | **React Three Fiber + drei** | Declarative, integrates with React reconciler, automatic cleanup |
| Spring-driven physical animation (hover bounce, drag inertia) | **R3F + @react-spring/three** | Tweens compose naturally with R3F |
| Designer hands you a scene, minimal code wanted | **Spline** (`@splinetool/react-spline`) | Visual editor → embeddable React component |
| Heavy game, WebXR, native physics, advanced PBR | **Babylon.js** with React | Full engine; expect ~46% more memory than three.js |
| Existing non-React app or you need full imperative control | Vanilla Three.js | Avoid inside React — see pitfall below |

If the user has already chosen a library, respect that choice and skip the selection step.

### The vanilla Three.js pitfall (important)

Do not instantiate `THREE.Scene`, meshes, or `WebGLRenderer` directly inside a React component without R3F. Every state change creates new instances; React doesn't know to dispose the old ones, and they accumulate as invisible CPU/GPU-resident objects until the tab crashes. R3F exists specifically to solve this — it hooks into React's reconciler so that mounting/unmounting a `<mesh>` correctly disposes geometries, materials, and textures.

If the user *insists* on vanilla Three.js inside React, they must:
1. Create the scene/renderer in a `useEffect` with empty deps, store in a ref.
2. Return a cleanup function that calls `renderer.dispose()`, `scene.traverse(o => { o.geometry?.dispose(); o.material?.dispose() })`, and removes the canvas from the DOM.
3. Drive updates by mutating the ref, never by re-creating the scene.

R3F handles all of this for free. Recommend it.

## Project setup

For a fresh React project, use Vite — fast HMR matters when you're iterating on visuals:

```bash
npm create vite@latest my-app -- --template react
cd my-app
npm install three @react-three/fiber @react-three/drei
# Optional, depending on need:
npm install @react-spring/three        # spring animations
npm install leva                        # debug GUI for tweaking values
npm install @react-three/postprocessing # bloom, depth-of-field, etc.
```

For Next.js, R3F components must be client components — add `"use client"` to any file that imports from `@react-three/fiber` or `@react-three/drei`. Put the `<Canvas>` in a leaf component and dynamic-import it with `ssr: false` if it touches `window`/WebGL at module scope.

## The minimal scene

Every R3F scene has the same skeleton. Internalize this — most user requests are variations on it.

```jsx
import { Canvas } from '@react-three/fiber'
import { OrbitControls } from '@react-three/drei'

export function Scene() {
  return (
    <Canvas camera={{ position: [3, 3, 3], fov: 50 }}>
      <ambientLight intensity={0.4} />
      <directionalLight position={[5, 5, 5]} intensity={1} castShadow />
      <mesh>
        <boxGeometry args={[1, 1, 1]} />
        <meshStandardMaterial color="orange" />
      </mesh>
      <OrbitControls />
    </Canvas>
  )
}
```

Key facts about JSX in R3F:
- Lowercase tags like `<mesh>`, `<boxGeometry>`, `<meshStandardMaterial>` map to Three.js classes (`THREE.Mesh`, `THREE.BoxGeometry`, ...). The mapping is by name; any Three.js class is reachable this way.
- `args` is the constructor argument array. `<boxGeometry args={[1, 1, 1]} />` → `new THREE.BoxGeometry(1, 1, 1)`.
- Props after `args` set instance properties: `position`, `rotation`, `scale`, plus class-specific ones like `color`, `roughness`.
- Children are added with `.add()`. So a `<mesh>` automatically gets its `<boxGeometry>` and `<meshStandardMaterial>` attached.

## Animation patterns

There are four idiomatic ways to animate. Pick by the kind of motion.

### 1. Continuous animation: `useFrame`

For things that move every frame — rotation, floating, follow-the-mouse, time-based shaders.

```jsx
import { useRef } from 'react'
import { useFrame } from '@react-three/fiber'

function SpinningBox() {
  const ref = useRef()
  useFrame((state, delta) => {
    ref.current.rotation.y += delta            // frame-rate independent
    ref.current.position.y = Math.sin(state.clock.elapsedTime) * 0.5
  })
  return (
    <mesh ref={ref}>
      <boxGeometry />
      <meshStandardMaterial color="hotpink" />
    </mesh>
  )
}
```

**Critical**: mutate the ref directly (`ref.current.rotation.y += delta`). Do **not** put per-frame values in `useState` — it would re-render the React tree 60 times a second and tank performance. R3F runs `useFrame` inside its own render loop, outside React reconciliation.

Use `delta` (seconds since last frame), not a fixed step, so motion is consistent across frame rates.

### 2. State-driven tweens: `@react-spring/three`

For animations that respond to React state (hover, click, route change). Springs feel physical, don't need duration tuning.

```jsx
import { useSpring, animated } from '@react-spring/three'
import { useState } from 'react'

function HoverCard() {
  const [hovered, setHovered] = useState(false)
  const { scale, color } = useSpring({
    scale: hovered ? 1.3 : 1,
    color: hovered ? '#ff6b6b' : '#4dabf7',
    config: { tension: 200, friction: 15 },
  })
  return (
    <animated.mesh
      scale={scale}
      onPointerOver={() => setHovered(true)}
      onPointerOut={() => setHovered(false)}
    >
      <boxGeometry />
      <animated.meshStandardMaterial color={color} />
    </animated.mesh>
  )
}
```

`animated.*` versions of R3F primitives subscribe to spring values without re-rendering React.

### 3. Pre-baked GLTF animations: `useAnimations`

When the user has a `.glb`/`.gltf` with embedded animations (skeletal, morph targets, baked transforms).

```jsx
import { useGLTF, useAnimations } from '@react-three/drei'
import { useEffect, useRef } from 'react'

function Character({ url }) {
  const group = useRef()
  const { scene, animations } = useGLTF(url)
  const { actions, names } = useAnimations(animations, group)
  useEffect(() => {
    actions[names[0]]?.reset().fadeIn(0.3).play()
  }, [actions, names])
  return <primitive ref={group} object={scene} />
}
```

For models with multiple clips, pick by name (`actions['Idle']`, `actions['Walk']`) and crossfade with `.fadeIn`/`.fadeOut`.

For static GLB without animations, just render `<primitive object={scene} />` and animate it with `useFrame` or springs.

### 4. Scroll-driven: drei's `<ScrollControls>` or framer-motion

```jsx
import { ScrollControls, useScroll } from '@react-three/drei'

function Scene() {
  return (
    <ScrollControls pages={3} damping={0.2}>
      <Content />
    </ScrollControls>
  )
}

function Content() {
  const ref = useRef()
  const scroll = useScroll()
  useFrame(() => {
    ref.current.rotation.y = scroll.offset * Math.PI * 2  // 0..1 across all pages
  })
  return <mesh ref={ref}>{/* ... */}</mesh>
}
```

## Reference files

For deeper, narrower topics, read the relevant file in `references/`:

- `references/tooling.md` — Detailed tool comparison (R3F vs Three.js vs Spline vs Babylon.js vs P5.js). Read when the user is asking which tool to pick or weighing trade-offs.
- `references/gltf-models.md` — Loading `.glb`/`.gltf`/`.fbx`/`.obj`, draco compression, KTX2 textures, file-upload viewers, `gltfjsx` codegen. Read when the user wants to load a 3D model file.
- `references/shaders.md` — Custom GLSL vertex/fragment shaders, `shaderMaterial` from drei, noise-driven displacement, `<Effects>` post-processing. Read when the user wants custom shaders, glow, distortion, dissolve, or any GLSL.
- `references/lighting-cameras.md` — Light types (ambient, directional, point, spot, hemisphere), shadow setup, perspective vs orthographic camera, `PresentationControls`, `CameraControls`. Read for visual quality / mood / framing questions.
- `references/performance.md` — Instanced meshes, on-demand rendering (`frameloop="demand"`), draco/meshopt, level-of-detail, suspense lazy-loading, mobile considerations. Read when the user mentions slowness, FPS, mobile, "many objects", or large scenes.
- `references/spline.md` — Embedding Spline scenes via `@splinetool/react-spline`, triggering events, sizing, fallbacks. Read when the user mentions Spline or wants a designer-built scene embedded.

## Output expectations

When the user asks for a working component, deliver:

1. The full component file (imports, JSX, exported function) — runnable as-is, dropped into a Vite or Next.js project that has `three`, `@react-three/fiber`, `@react-three/drei` installed.
2. The exact `npm install` line for any *additional* packages used beyond those three.
3. If using Next.js patterns (`"use client"`, `dynamic` with `ssr: false`), include them — a silent SSR crash is the most common newcomer trap.
4. A `<Canvas>` wrapper if the user is creating a top-level scene; just the inner mesh component if they're building a piece to drop into an existing canvas.

Skip lengthy prose. Show the code, then briefly call out anything non-obvious (a frame-loop subtlety, a known gotcha with their model format, a perf consideration).

## Common gotchas, recap

- Don't drive per-frame values through `useState` — mutate refs inside `useFrame`.
- Don't instantiate vanilla Three.js objects inside a React component — leaks memory.
- In Next.js, R3F needs `"use client"`. Dynamic-import with `ssr: false` if you touch `window` at module scope.
- `useGLTF`/`useTexture` suspend — wrap consumers in `<Suspense fallback={...}>` (or use drei's `<Loader />` overlay).
- For shadows, set `shadows` on `<Canvas>`, `castShadow` on lights and meshes that cast, `receiveShadow` on meshes that receive. Forgetting any of these silently disables shadows.
- `<color attach="background" args={['#000']} />` to set scene background; `attach="background"` is easy to forget.
