// Shown immediately when opening a recipe, while the API (or a paused Aurora) responds.
// loading.tsx receives no params, so the busy state is announced without locale-specific text.
export default function Loading() {
  return (
    <article className="detail" aria-busy="true">
      <div className="skeleton skeleton-line short" />
      <div className="detail-img skeleton skeleton-hero" />
      <div className="detail-header">
        <div className="skeleton skeleton-line short" />
        <div className="skeleton skeleton-title" />
        <div className="skeleton skeleton-line" />
      </div>
    </article>
  );
}
