import React from "react";
import ReactDOM from "react-dom/client";

function App() {
  return (
    <main style={{
      fontFamily: "Arial, sans-serif",
      minHeight: "100vh",
      padding: "48px",
      background: "#f7f9fc",
      color: "#1f2937"
    }}>
      <div style={{
        maxWidth: 960,
        margin: "0 auto",
        background: "white",
        borderRadius: 24,
        padding: 32,
        boxShadow: "0 10px 30px rgba(0,0,0,0.08)"
      }}>
        <p style={{ margin: 0, fontSize: 14, opacity: 0.7 }}>TekAttend by Tekforge</p>
        <h1 style={{ fontSize: 40, margin: "8px 0 12px" }}>Presença inteligente para aulas</h1>
        <p style={{ fontSize: 18, lineHeight: 1.5, maxWidth: 720 }}>
          Estrutura inicial do frontend do TekAttend. O próximo passo é evoluir esta base
          para landing page, login e painel do professor.
        </p>

        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))", gap: 16, marginTop: 28 }}>
          <section style={{ padding: 20, border: "1px solid #e5e7eb", borderRadius: 18 }}>
            <h2 style={{ fontSize: 20 }}>Professor</h2>
            <p>Abrir chamada, confirmar solicitações e exportar relatórios.</p>
          </section>
          <section style={{ padding: 20, border: "1px solid #e5e7eb", borderRadius: 18 }}>
            <h2 style={{ fontSize: 20 }}>Aluno</h2>
            <p>Solicitar presença, acompanhar confirmação e avaliar a aula.</p>
          </section>
          <section style={{ padding: 20, border: "1px solid #e5e7eb", borderRadius: 18 }}>
            <h2 style={{ fontSize: 20 }}>Infra</h2>
            <p>Cloud Run, Firestore, Storage e automação com GitHub Actions.</p>
          </section>
        </div>
      </div>
    </main>
  );
}

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
