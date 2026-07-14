import type { Locale } from "./locales.ts";

export type LocaleCopy = {
  version: "1.0.0";
  language: string;
  theme: string;
  system: string;
  light: string;
  dark: string;
  home: string;
  docs: string;
  quickStart: string;
  changelog: string;
  eyebrow: string;
  title: string;
  subtitle: string;
  getStarted: string;
  viewGitHub: string;
  fallback: string;
  luxLabel: string;
  evidenceTitle: string;
  problemTitle: string;
  helpTitle: string;
  workflowTitle: string;
  profilesTitle: string;
  filesTitle: string;
  trustTitle: string;
  finalTitle: string;
};

export const localeNames: Record<Locale, string> = {
  "en-US": "English (US)",
  "pt-BR": "Português (Brasil)",
};

export const translations: Record<Locale, LocaleCopy> = {
  "en-US": {
    version: "1.0.0",
    language: "Language",
    theme: "Theme",
    system: "System",
    light: "Light",
    dark: "Dark",
    home: "Home",
    docs: "Documentation",
    quickStart: "Quick start",
    changelog: "Changelog",
    eyebrow: "Development with project context",
    title: "Keep AI-assisted development grounded in your project.",
    subtitle:
      "Give Claude Code and Codex the context, instructions, and checks they need to make changes that belong in your codebase.",
    getStarted: "Start the guided setup",
    viewGitHub: "View on GitHub",
    fallback:
      "This content is not available in your language yet. Showing English.",
    luxLabel: "Lux, your development companion",
    evidenceTitle: "Every command stays tied to the reasons behind the change.",
    problemTitle: "AI moves fast. Your project context does not come along.",
    helpTitle:
      "A shared source of truth both assistants read before they touch a file.",
    workflowTitle: "Five steps, from start to synchronized.",
    profilesTitle: "Share the setup that already works for your team.",
    filesTitle: "Plain files, committed to your repository. Nothing hidden.",
    trustTitle: "Runs on your machine. On your terms.",
    finalTitle: "Set up your project in one command.",
  },
  "pt-BR": {
    version: "1.0.0",
    language: "Idioma",
    theme: "Tema",
    system: "Sistema",
    light: "Claro",
    dark: "Escuro",
    home: "Início",
    docs: "Documentação",
    quickStart: "Início rápido",
    changelog: "Histórico de mudanças",
    eyebrow: "Desenvolvimento com o contexto do projeto",
    title:
      "Mantenha o desenvolvimento assistido por IA fundamentado no seu projeto.",
    subtitle:
      "Dê ao Claude Code e ao Codex o contexto, as instruções e as verificações necessárias para fazer mudanças que pertencem à sua base de código.",
    getStarted: "Iniciar configuração guiada",
    viewGitHub: "Ver no GitHub",
    fallback:
      "Este conteúdo ainda não está disponível no seu idioma. Exibindo em inglês.",
    luxLabel: "Lux, seu companheiro de desenvolvimento",
    evidenceTitle:
      "Cada comando permanece ligado aos motivos por trás da mudança.",
    problemTitle:
      "A IA avança rápido. O contexto do seu projeto não a acompanha.",
    helpTitle:
      "Uma fonte compartilhada de verdade que ambos os assistentes leem antes de alterar um arquivo.",
    workflowTitle: "Cinco etapas, do início à sincronização.",
    profilesTitle:
      "Compartilhe a configuração que já funciona para sua equipe.",
    filesTitle:
      "Arquivos simples, versionados no seu repositório. Nada oculto.",
    trustTitle: "Executado na sua máquina. Nos seus termos.",
    finalTitle: "Configure seu projeto com um comando.",
  },
};
