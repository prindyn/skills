# Custom shaders and post-processing

For visual effects beyond what built-in materials provide — animated displacement, dissolve, hologram, custom lighting, glow, color grading.

## When to write a shader vs use a built-in material

Try built-ins first. Many "shader-y" effects are achievable with:

- `meshPhysicalMaterial` — clearcoat, sheen, transmission, iridescence (PBR).
- `MeshTransmissionMaterial` from drei — glass, ice, refraction.
- `MeshDistortMaterial` from drei — animated noise displacement (good for blob/jelly).
- `MeshWobbleMaterial` from drei — animated wobble.
- Drei's `Sparkles`, `Cloud`, `Stars` — particle effects.

Write a custom shader when those don't cover it: dissolve transitions, custom data-driven coloring, vertex animation tied to state, hologram/scanline, edge highlight, etc.

## Custom shaders with drei's `shaderMaterial`

`shaderMaterial` is a factory that turns GLSL strings + uniforms into a reusable material component. This is the path of least resistance.

```jsx
import { shaderMaterial } from '@react-three/drei'
import { extend, useFrame } from '@react-three/fiber'
import * as THREE from 'three'
import { useRef } from 'react'

const WaveMaterial = shaderMaterial(
  // Uniforms
  { uTime: 0, uColor: new THREE.Color('#4dabf7') },
  // Vertex shader
  /* glsl */ `
    uniform float uTime;
    varying vec2 vUv;
    void main() {
      vUv = uv;
      vec3 p = position;
      p.z += sin(p.x * 4.0 + uTime) * 0.2;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(p, 1.0);
    }
  `,
  // Fragment shader
  /* glsl */ `
    uniform vec3 uColor;
    varying vec2 vUv;
    void main() {
      gl_FragColor = vec4(uColor * (0.5 + vUv.y * 0.5), 1.0);
    }
  `,
)

extend({ WaveMaterial })   // makes <waveMaterial /> available as JSX

export function WavePlane() {
  const ref = useRef()
  useFrame((state) => {
    ref.current.uTime = state.clock.elapsedTime
  })
  return (
    <mesh>
      <planeGeometry args={[3, 3, 64, 64]} />
      <waveMaterial ref={ref} />
    </mesh>
  )
}
```

A few notes:

- `extend({ WaveMaterial })` exposes the class as `<waveMaterial />` — lowercase first letter when using as JSX.
- Uniforms become props (`<waveMaterial uTime={...} uColor={...} />`) and ref properties (`ref.current.uTime = ...`). Mutating via the ref in `useFrame` is faster than passing as a prop.
- For TypeScript, you'll need to augment the JSX namespace; for a quick start, JS or non-strict TS is easier.
- The `/* glsl */` template tag is a hint for editor extensions to enable GLSL syntax highlighting — purely cosmetic.

## Noise-based vertex displacement

The classic "animated blob" effect uses a noise function in the vertex shader to displace position. Bring in `glsl-noise` via webpack/vite, or paste a Simplex/Perlin function directly into the shader source.

```glsl
// Top of the vertex shader
// (paste a noise function — common ones: snoise(vec3), pnoise(vec3) from webgl-noise/lygia)

uniform float uTime;
uniform float uIntensity;
varying vec3 vNormal;

void main() {
  vec3 p = position;
  float n = snoise(p * 1.5 + uTime * 0.3);
  p += normal * n * uIntensity;
  vNormal = normalize(normalMatrix * normal);
  gl_Position = projectionMatrix * modelViewMatrix * vec4(p, 1.0);
}
```

Pair with a sphere with high segment count (`<sphereGeometry args={[1, 128, 128]} />`) so there are enough vertices to displace smoothly.

For a copy-paste noise function, the `lygia` shader library and Inigo Quilez's site (iquilezles.org) are good sources. Reference but inline the function — don't import GLSL across files unless you've set up a glsl loader.

## Dissolve / clip / reveal

Useful for entrance and exit animations:

```glsl
uniform float uProgress;     // 0..1
varying vec2 vUv;

void main() {
  float threshold = 1.0 - uProgress;
  // discard pixels where some noise/gradient is below threshold
  if (vUv.y < threshold) discard;
  gl_FragColor = vec4(1.0);
}
```

Drive `uProgress` from React state via spring or `useFrame`.

## Post-processing: bloom, depth-of-field, vignette

`@react-three/postprocessing` wraps `pmndrs/postprocessing` for R3F:

```bash
npm install @react-three/postprocessing
```

```jsx
import { EffectComposer, Bloom, ChromaticAberration, Vignette } from '@react-three/postprocessing'

<Canvas>
  {/* scene */}
  <EffectComposer>
    <Bloom intensity={0.6} luminanceThreshold={0.4} />
    <ChromaticAberration offset={[0.001, 0.001]} />
    <Vignette eskil={false} offset={0.1} darkness={0.6} />
  </EffectComposer>
</Canvas>
```

For bloom to fire on specific objects, set `meshStandardMaterial`'s `emissive` color and `emissiveIntensity > 1` (HDR), and set `<Bloom luminanceThreshold={1}>`.

## Quick recipes

- **Glow**: emissive material + bloom post-process.
- **Hologram**: fragment shader with `sin(vUv.y * 100.0 + uTime * 5.0)` scanlines + transparency + additive blending.
- **Toon**: drei's `<MeshToonMaterial>` + a 1D ramp texture.
- **Outline**: drei's `<Outlines />` component — just nest under a mesh.
- **Wobble blob**: drei's `<MeshDistortMaterial distort={0.4} speed={2}>` — no custom GLSL needed.
