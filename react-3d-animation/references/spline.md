# Spline scenes in React

Spline (spline.design) is a visual 3D editor. Designers build a scene with built-in animations, hover/click states, and physics, and export it as a hosted scene. The React integration is `@splinetool/react-spline`.

```bash
npm install @splinetool/react-spline @splinetool/runtime
```

## Basic embed

```jsx
import Spline from '@splinetool/react-spline'

export function Hero() {
  return (
    <Spline scene="https://prod.spline.design/your-scene-id/scene.splinecode" />
  )
}
```

The scene URL comes from Spline's "Export → Code → React" flow.

## Sizing

Spline's `<Spline />` renders a canvas that fills its parent. Wrap in a sized container:

```jsx
<div style={{ width: '100%', height: '100vh' }}>
  <Spline scene={url} />
</div>
```

Without a sized parent, the canvas collapses to 0 height.

## Triggering events from React

Use `onLoad` to grab the scene's API, then call `emitEvent` or read `findObjectByName`:

```jsx
import Spline from '@splinetool/react-spline'
import { useRef } from 'react'

export function InteractiveHero() {
  const splineRef = useRef()

  const onLoad = (spline) => { splineRef.current = spline }

  const triggerSpin = () => {
    splineRef.current?.emitEvent('mouseDown', 'Cube')
    // or look up by ID:
    // const obj = splineRef.current.findObjectById('uuid-from-spline-editor')
  }

  return (
    <>
      <Spline scene="..." onLoad={onLoad} />
      <button onClick={triggerSpin}>Spin</button>
    </>
  )
}
```

The event names (`mouseDown`, `mouseHover`, `keyDown`, `start`, `lookAt`) and target object names match what's set up in the Spline editor.

## Reading state out of Spline

```jsx
const onSplineMouseDown = (e) => {
  // e.target is the Spline object that was clicked
  console.log('clicked', e.target.name)
}

<Spline scene={url} onMouseDown={onSplineMouseDown} />
```

Other callbacks: `onMouseUp`, `onMouseHover`, `onKeyDown`, `onKeyUp`, `onStart`, `onLookAt`, `onFollow`.

## Loading state and fallback

`<Spline>` doesn't show anything until the scene loads. Add an `onLoad` to flip a loading flag, or place a skeleton/poster underneath:

```jsx
const [loaded, setLoaded] = useState(false)

<div className="hero">
  {!loaded && <img src="/poster.jpg" alt="" className="poster" />}
  <Spline scene={url} onLoad={() => setLoaded(true)} />
</div>
```

Spline scenes can be 1-5MB+ (geometry, textures, runtime). Always pair with a poster or explicit loading UI.

## When NOT to use Spline

- The user wants tight code-level control over animations or per-frame logic — use R3F instead.
- Bundle size is critical (Spline runtime adds ~150KB plus scene weight) — R3F can be more selective about what's pulled in.
- The scene needs to react to data that changes frequently (e.g. live charts in 3D) — Spline's event API isn't built for high-frequency updates.

## When Spline is the right choice

- Marketing pages where a designer is iterating visually.
- Static-ish hero sections with self-contained interactions.
- "Make it look cool" briefs where build-time matters more than runtime fidelity.
- Mixing Spline scenes with R3F is also valid — you can have a Spline hero and a separate R3F gallery.
