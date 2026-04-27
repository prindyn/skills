# Lighting and cameras

## Light types

A scene with no lights renders everything black except materials that don't use lighting (`meshBasicMaterial`). The standard starter set is **ambient + directional**.

| Light | What it does | When to use |
|---|---|---|
| `<ambientLight intensity={0.4} />` | Equal light from every direction. No shadows, no direction cues. | Always include a low-intensity ambient (~0.2–0.5) so surfaces in shadow aren't black. |
| `<directionalLight position={[5,5,5]} intensity={1} castShadow />` | Parallel rays from a direction. Fast, casts shadows. Position is direction, not point. | Default key light. Use for sun, main light source. |
| `<pointLight position={[0,2,0]} intensity={5} distance={10} decay={2} />` | Omnidirectional from a point, falls off with distance (inverse-square when `decay={2}`). | Lamps, candles, torches, localized glow. |
| `<spotLight position={[0,5,0]} angle={0.3} penumbra={0.5} intensity={10} castShadow />` | Cone of light. | Stage lighting, flashlight, focused highlights. |
| `<hemisphereLight args={['#aaccff','#553311',0.6]} />` | Two-color gradient light (sky + ground). | Outdoor scenes, soft fill. |
| `<rectAreaLight width={2} height={2} intensity={5} />` | Soft area light. Doesn't cast shadows. Needs `RectAreaLightUniformsLib.init()` once. | Studio softbox look, screen/window light. |

## Three-point lighting recipe

A clean starter for product showcases:

```jsx
<ambientLight intensity={0.3} />
<directionalLight position={[5, 5, 5]} intensity={1.0} castShadow />   {/* key */}
<directionalLight position={[-5, 3, 2]} intensity={0.5} />              {/* fill */}
<directionalLight position={[0, 4, -5]} intensity={0.3} />              {/* rim */}
```

Or use drei's `<Environment preset="studio" />` to skip lighting entirely and just use HDRI image-based lighting:

```jsx
import { Environment } from '@react-three/drei'

<Environment preset="city" />
// presets: apartment, city, dawn, forest, lobby, night, park, studio, sunset, warehouse
```

`<Environment background />` also uses the HDRI as the visible background.

## Shadows

Three pieces all required, easy to forget any one:

1. `<Canvas shadows>` — enables shadow rendering globally.
2. Lights that cast shadows need `castShadow`. Only `directionalLight`, `spotLight`, `pointLight` cast.
3. Meshes need `castShadow` (object blocks light) and/or `receiveShadow` (object shows shadows on its surface).

```jsx
<Canvas shadows>
  <directionalLight position={[5,5,5]} castShadow shadow-mapSize={[2048, 2048]} />
  <mesh castShadow>{/* the casting object */}</mesh>
  <mesh receiveShadow>
    <planeGeometry args={[20, 20]} />
    <meshStandardMaterial color="white" />
  </mesh>
</Canvas>
```

For directional lights, the shadow camera is orthographic and has limited extent — out-of-frame areas don't get shadows. Tune via `shadow-camera-left/right/top/bottom`:

```jsx
<directionalLight
  castShadow
  position={[5, 5, 5]}
  shadow-camera-left={-10}
  shadow-camera-right={10}
  shadow-camera-top={10}
  shadow-camera-bottom={-10}
/>
```

For soft contact shadows under an object (cheap and good-looking), use drei's `<ContactShadows>`:

```jsx
<ContactShadows position={[0, -0.5, 0]} opacity={0.5} scale={5} blur={2} far={2} />
```

## Cameras

R3F's `<Canvas>` creates a `PerspectiveCamera` by default. Configure via the `camera` prop:

```jsx
<Canvas camera={{ position: [3, 3, 3], fov: 50, near: 0.1, far: 100 }}>
```

For an orthographic camera (CAD-like, no perspective foreshortening):

```jsx
<Canvas orthographic camera={{ zoom: 50, position: [10, 10, 10] }}>
```

To switch cameras dynamically, use drei's `<PerspectiveCamera makeDefault>` or `<OrthographicCamera makeDefault>` inside the canvas.

## Camera controls (user navigation)

| Component | Behavior |
|---|---|
| `<OrbitControls />` | Drag to rotate around target, scroll to zoom, right-drag to pan. The 90% choice. |
| `<MapControls />` | Like OrbitControls but with pan as primary (left-drag). For top-down map views. |
| `<TrackballControls />` | Free rotation, no fixed up vector. |
| `<PresentationControls />` | Constrained drag with snap-back. Good for product cards — user can wiggle the model but it returns to a hero pose. |
| `<CameraControls />` | Powerful imperative controller (drei wraps `camera-controls` package). Use when you need programmatic camera moves with smooth interpolation. |
| `<ScrollControls />` + `useScroll()` | Scroll position drives camera/scene. See SKILL.md scroll example. |

`PresentationControls` defaults that work well for product hero:

```jsx
<PresentationControls
  global
  config={{ mass: 2, tension: 500 }}
  snap={{ mass: 4, tension: 1500 }}
  rotation={[0, 0, 0]}
  polar={[-Math.PI / 4, Math.PI / 4]}
  azimuth={[-Math.PI / 4, Math.PI / 4]}
>
  <Model />
</PresentationControls>
```

## Programmatic camera animation

For cinematic moves, animate the camera via `useFrame` against a target, or use drei's `<CameraControls>`:

```jsx
import { CameraControls } from '@react-three/drei'
import { useEffect, useRef } from 'react'

function CinematicIntro() {
  const cc = useRef()
  useEffect(() => {
    cc.current.setLookAt(10, 10, 10, 0, 0, 0, false)        // start
    cc.current.setLookAt(2, 1, 2, 0, 0.5, 0, true)          // animate to
  }, [])
  return <CameraControls ref={cc} />
}
```

Third arg `true` = animate (default damping interpolation). `false` = snap.
