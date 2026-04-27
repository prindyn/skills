# Loading and animating GLTF/GLB/FBX/OBJ models

GLB/GLTF is the format you should push for — it's the standard, supports embedded animations, materials, and textures, and is what `useGLTF` is optimized for. FBX and OBJ work but have rougher edges.

## Static GLB

```jsx
import { useGLTF } from '@react-three/drei'

function Model({ url }) {
  const { scene } = useGLTF(url)
  return <primitive object={scene} />
}

useGLTF.preload('/models/duck.glb')   // optional: warm cache before render
```

`useGLTF` suspends, so wrap consumers in `<Suspense>`:

```jsx
<Canvas>
  <Suspense fallback={null}>
    <Model url="/models/duck.glb" />
  </Suspense>
</Canvas>
```

For a polished loading state, drei ships `<Loader />` (renders an HTML overlay outside the canvas):

```jsx
import { Loader } from '@react-three/drei'

<Canvas>{/* ... */}</Canvas>
<Loader />
```

## GLB with embedded animations

```jsx
import { useGLTF, useAnimations } from '@react-three/drei'
import { useEffect, useRef } from 'react'

function AnimatedModel({ url, clipName }) {
  const group = useRef()
  const { scene, animations } = useGLTF(url)
  const { actions, mixer } = useAnimations(animations, group)

  useEffect(() => {
    const action = actions[clipName] ?? Object.values(actions)[0]
    action?.reset().fadeIn(0.3).play()
    return () => { action?.fadeOut(0.3) }
  }, [actions, clipName])

  return <primitive ref={group} object={scene} />
}
```

To switch animations without restarting from frame 0, keep both actions playing with cross-fade:

```jsx
useEffect(() => {
  const next = actions[clipName]
  const prev = previousAction.current
  if (prev && prev !== next) prev.fadeOut(0.3)
  next?.reset().fadeIn(0.3).play()
  previousAction.current = next
}, [clipName])
```

## FBX

```jsx
import { useFBX } from '@react-three/drei'

function FbxModel({ url }) {
  const fbx = useFBX(url)
  return <primitive object={fbx} />
}
```

FBX often arrives with bizarre scales (centimeters vs meters) — be ready to add `scale={0.01}`. Materials may not survive the FBX export cleanly; many users replace them after load:

```jsx
fbx.traverse((o) => { if (o.isMesh) o.material = new THREE.MeshStandardMaterial({ color: 'gray' }) })
```

## OBJ

```jsx
import { useLoader } from '@react-three/fiber'
import { OBJLoader } from 'three/examples/jsm/loaders/OBJLoader.js'

function ObjModel({ url }) {
  const obj = useLoader(OBJLoader, url)
  return <primitive object={obj} />
}
```

OBJ has no animation support and limited material support (`.mtl` sidecar file required for materials). For modern work, prefer GLB.

## User-uploaded models (file picker / drag-and-drop)

The pattern: read the file as an `ArrayBuffer` or object URL, then feed it to the appropriate loader.

```jsx
import { useState } from 'react'
import { Canvas } from '@react-three/fiber'
import { useGLTF, OrbitControls } from '@react-three/drei'
import { Suspense } from 'react'

function UploadedModel({ url }) {
  const { scene } = useGLTF(url)
  return <primitive object={scene} />
}

export function ModelViewer() {
  const [url, setUrl] = useState(null)

  const onPick = (e) => {
    const file = e.target.files?.[0]
    if (!file) return
    setUrl((prev) => {
      if (prev) URL.revokeObjectURL(prev)
      return URL.createObjectURL(file)
    })
  }

  return (
    <>
      <input type="file" accept=".glb,.gltf" onChange={onPick} />
      <Canvas camera={{ position: [3, 3, 3] }}>
        <ambientLight />
        <directionalLight position={[5, 5, 5]} />
        <Suspense fallback={null}>
          {url && <UploadedModel url={url} />}
        </Suspense>
        <OrbitControls />
      </Canvas>
    </>
  )
}
```

Always `URL.revokeObjectURL` the previous blob URL when replacing — otherwise the browser holds the file in memory.

For multi-file GLTFs (`.gltf` + textures + `.bin`), object URLs alone won't resolve sibling references. Either zip-and-extract on the client or insist on `.glb` (single file).

## Compression: draco and meshopt

Production GLBs are usually compressed. `useGLTF` handles draco transparently if you point it at the decoder:

```jsx
import { useGLTF } from '@react-three/drei'
useGLTF.setDecoderPath('https://www.gstatic.com/draco/v1/decoders/')
```

For meshopt, install `meshoptimizer` and set:

```js
import { MeshoptDecoder } from 'three/examples/jsm/libs/meshopt_decoder.module.js'
useGLTF.setMeshoptDecoder(MeshoptDecoder)
```

## Codegen: gltfjsx

`npx gltfjsx model.glb` generates a typed React component with every node and material exposed individually. Useful when:

- You want to apply different materials to specific meshes.
- You want to animate or hide individual sub-meshes.
- You want types/autocomplete for the model's structure.

The output is regular JSX — drop it in, edit nodes/materials freely.

## Centering and scaling

Models often arrive with the origin not at their visual center, or at an awkward scale. Two tricks:

```jsx
import { Center, Bounds } from '@react-three/drei'

// Auto-center: shifts geometry so visual center is at the local origin.
<Center>
  <Model url="/x.glb" />
</Center>

// Auto-fit: zooms camera to frame contents.
<Bounds fit clip observe>
  <Model url="/x.glb" />
</Bounds>
```
