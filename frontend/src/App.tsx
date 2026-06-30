function App() {
  return (
    <main className="app">
      <section className="hero">
        <h1>Coffee House</h1>
        <p>
          Онлайн-заявки, бронирование и админ-панель для кофейни.
        </p>

        <div className="hero__actions">
          <a href="/booking" className="button">
            Забронировать
          </a>
          <a href="/admin/login" className="button button--secondary">
            Админ-панель
          </a>
        </div>
      </section>
    </main>
  )
}

export default App