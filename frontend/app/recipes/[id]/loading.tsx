// Shown immediately when opening a recipe, while the API (or a paused Aurora) responds
export default function Loading() {
  return (
    <article className="detail" aria-busy="true" aria-label="読み込み中">
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
