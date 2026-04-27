# Performance

3D in a browser is GPU-bound; the usual React perf tools (memo, virtualization) only help with the React-side overhead. Most wins come from doing less rendering work or sending less data to the GPU.

## On-demand rendering

By default `<Canvas>` runs at 60fps regardless of whether anything's changed. For a static scene with occasional interactions, switch to demand mode:

```jsx
<Canvas frameloop="demand">
```

The canvas only renders when invalidated. R3F invalidates automatically when controls move, when `useFrame` runs (so don't use `useFrame` if you want this mode to actually save frames), or when you call `invalidate()` from `useThree`.

For a hybrid (always-on while controls are interacted with, idle otherwise), `<OrbitControls regress />` with `<PerformanceMonitor>` from drei.

## Instancing

When you have many copies of the same mesh (trees, particles, stars, bricks), don't render them as separate components — use instancing. One draw call instead of N.

```jsx
import { Instances, Instance } from '@react-three/drei'

<Instances limit={1000}>
  <boxGeometry />
  <meshStandardMaterial />
  {positions.map((p, i) => (
    <Instance key={i} position={p} color={colors[i]} />
  ))}
</Instances>
```

For tens of thousands, drop to `THREE.InstancedMesh` directly via R3F:

```jsx
import { useMemo } from 'react'
import * as THREE from 'three'

function Forest({ count = 5000 }) {
  const ref = useRef()
  useEffect(() => {
    const m = new THREE.Matrix4()
    for (let i = 0; i < count; i++) {
      m.setPosition(Math.random() * 100, 0, Math.random() * 100)
      ref.current.setMatrixAt(i, m)
    }
    ref.current.instanceMatrix.needsUpdate = true
  }, [count])
  return (
    <instancedMesh ref={ref} args={[null, null, count]}>
      <coneGeometry args={[0.3, 1, 6]} />
      <meshStandardMaterial color="green" />
    </instancedMesh>
  )
}
```

## Mesh and texture compression

- **Draco** for geometry (often 5–10× smaller). `gltf-transform optimize input.glb output.glb`.
- **Meshopt** as an alternative; sometimes better for animated meshes.
- **KTX2 (Basis)** for textures (4–8× smaller, GPU-native compressed format that uses less VRAM at runtime).

`gltf-transform` (Don McCurdy's CLI) handles all three:

```bash
npx gltf-transform optimize in.glb out.glb --texture-compress webp --simplify
```

## Level of detail (LOD)

Swap geometry detail based on camera distance. Drei has `<Lod>`:

```jsx
import { Lod } from '@react-three/drei'

<Lod distances={[0, 10, 50]}>
  <DetailedMesh />     {/* near */}
  <MidMesh />
  <FarMesh />          {/* far */}
</Lod>
```

## Don't re-render React when it's avoidable

- Per-frame state goes in refs, not `useState`.
- Hover/click state can stay in React, but don't put `position` or `rotation` in state if `useFrame` is going to write to it anyway.
- Keep `<Canvas>` props stable — passing a new object literal every render (`camera={{position: [...]}}`) is fine because R3F shallow-compares, but passing an unstable function to `onCreated` will re-mount the canvas.
- Memoize geometries/materials that you create in JS (not via JSX): `const geom = useMemo(() => new THREE.BoxGeometry(), [])`. JSX-created ones are auto-memoized by R3F.

## Suspense and lazy loading

Heavy components (large GLBs, post-processing) should be code-split:

```jsx
const HeavyScene = lazy(() => import('./HeavyScene'))

<Canvas>
  <Suspense fallback={<LightweightFallback />}>
    <HeavyScene />
  </Suspense>
</Canvas>
```

## Mobile considerations

- **Pixel ratio**: cap at 2 to avoid burning fillrate on Retina/high-DPI: `<Canvas dpr={[1, 2]}>`.
- **Shadows**: turn off on mobile or use `<ContactShadows>` (a single fake) instead of real shadow maps.
- **Post-processing**: bloom/SSAO are expensive — gate behind a tier check.
- **Battery**: pair `frameloop="demand"` with autoplay-pause when the tab is hidden (handled by browsers automatically for requestAnimationFrame).

A pragmatic mobile guard:

```jsx
const isLowPower = window.matchMedia('(max-width: 768px)').matches

<Canvas dpr={[1, isLowPower ? 1.5 : 2]} shadows={!isLowPower}>
  {/* ... */}
  {!isLowPower && <EffectComposer><Bloom /></EffectComposer>}
</Canvas>
```

## Profiling

- **drei `<Stats />`** — drops a stats.js panel showing FPS, frame time, MB. First thing to add when investigating.
- **drei `<PerformanceMonitor>`** — calls a callback when FPS drops; you can downgrade quality dynamically.
- **Chrome DevTools Performance tab** — flame chart shows JS time vs GPU time.
- **`renderer.info`** — accessible via `useThree(s => s.gl).info`. Reports draw calls, triangles, geometries, textures.
