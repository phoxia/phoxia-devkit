import type { Locale } from "./locales.ts";

export type LegalSection = { id: string; title: string; content: string };
export type LegalPageCopy = {
  title: string;
  updated: string;
  status: string;
  contents: string;
  sections: LegalSection[];
};

type LegalPages = { privacy: LegalPageCopy; terms: LegalPageCopy };

export const legalTranslations: Record<Locale, LegalPages> = {
  "en-US": {
    privacy: {
      title: "Privacy Policy",
      updated: "Last updated: July 14, 2026 · Draft 1.0",
      status: "Draft pending legal review",
      contents: "Contents",
      sections: [
        { id: "scope", title: "1. Scope and controller", content: "This policy covers kit.phoxia.org, the public website for Phoxia DevKit. Phoxia, operated by Lucas Christian, is responsible for this website. Privacy inquiries: privacy@phoxia.org." },
        { id: "website-data", title: "2. Website data", content: "The Kit website does not provide user accounts or payment features. Infrastructure providers may process technical request data needed to deliver, secure, and operate the website under their own policies and applicable agreements. This policy does not claim a fixed retention period that Phoxia has not independently verified." },
        { id: "preferences", title: "3. Browser preferences", content: "The website stores your language and theme preferences in your browser. These preferences remain on your device and can be removed through your browser storage controls." },
        { id: "devkit", title: "4. DevKit local behavior", content: "Installing or using Phoxia DevKit is separate from visiting this website. The DevKit setup reads and writes project files locally. The published setup workflow does not require a Phoxia account and does not upload source code to Phoxia." },
        { id: "third-parties", title: "5. External services", content: "Links to GitHub, Discord, and email open services operated by third parties. Information you send to those services is handled under their terms and privacy policies." },
        { id: "rights", title: "6. Your rights", content: "Depending on applicable law, including the LGPD and GDPR, you may request access, correction, deletion, portability, or information about personal data processing. Send requests to privacy@phoxia.org." },
        { id: "changes", title: "7. Changes and contact", content: "Material changes will update the date on this page and the public phoxia-devkit repository. Privacy: privacy@phoxia.org. Security reports: security@phoxia.org. General support: support@phoxia.org." },
      ],
    },
    terms: {
      title: "Terms of Use",
      updated: "Last updated: July 14, 2026 · Draft 1.0",
      status: "Draft pending legal review",
      contents: "Contents",
      sections: [
        { id: "scope", title: "1. Scope", content: "These terms govern access to kit.phoxia.org and its public information about Phoxia DevKit. The DevKit software is distributed separately under its repository license." },
        { id: "use", title: "2. Acceptable use", content: "You may use the website for lawful purposes. You may not attempt unauthorized access, disrupt availability, distribute malicious content, or impersonate Phoxia or its contributors." },
        { id: "license", title: "3. Open-source license", content: "Phoxia DevKit source code is distributed under the GNU Affero General Public License v3.0, AGPLv3. Your rights to use, study, modify, and distribute the software are governed by the license text in the phoxia-devkit repository." },
        { id: "content", title: "4. Website content", content: "Website and documentation content is provided for informational purposes and may change as the DevKit evolves. Project instructions, accepted RFCs, schemas, releases, and repository license files remain authoritative." },
        { id: "third-parties", title: "5. Third-party links", content: "The website links to external services including GitHub and Discord. Phoxia does not control their availability, security, content, terms, or privacy practices." },
        { id: "disclaimer", title: "6. Disclaimer", content: "To the extent permitted by applicable law, the website and software are provided as available and without warranties beyond those that cannot legally be excluded. Review generated changes before applying them to a repository." },
        { id: "liability", title: "7. Limitation and applicable law", content: "Liability is limited to the extent permitted by applicable law. These terms are governed by the laws of Brazil, without limiting mandatory rights that apply where you live." },
        { id: "changes", title: "8. Changes and contact", content: "Material changes will update the date on this page and the public phoxia-devkit repository. Legal questions: legal@phoxia.org. Privacy: privacy@phoxia.org. Support: support@phoxia.org." },
      ],
    },
  },
  "pt-BR": {
    privacy: {
      title: "Política de Privacidade",
      updated: "Última atualização: 14 de julho de 2026 · Minuta 1.0",
      status: "Minuta pendente de revisão jurídica",
      contents: "Conteúdo",
      sections: [
        { id: "scope", title: "1. Escopo e controlador", content: "Esta política cobre o kit.phoxia.org, site público do Phoxia DevKit. A Phoxia, operada por Lucas Christian, é responsável por este site. Questões de privacidade: privacy@phoxia.org." },
        { id: "website-data", title: "2. Dados do site", content: "O site do Kit não oferece contas de usuário nem recursos de pagamento. Provedores de infraestrutura podem tratar dados técnicos de requisição necessários para entregar, proteger e operar o site, conforme suas próprias políticas e os acordos aplicáveis. Esta política não declara um prazo fixo de retenção que a Phoxia não tenha verificado de forma independente." },
        { id: "preferences", title: "3. Preferências do navegador", content: "O site armazena suas preferências de idioma e tema no navegador. Essas preferências permanecem no seu dispositivo e podem ser removidas pelos controles de armazenamento do navegador." },
        { id: "devkit", title: "4. Comportamento local do DevKit", content: "Instalar ou usar o Phoxia DevKit é diferente de visitar este site. A configuração do DevKit lê e grava arquivos do projeto localmente. O fluxo publicado não exige uma conta Phoxia e não envia código-fonte para a Phoxia." },
        { id: "third-parties", title: "5. Serviços externos", content: "Links para GitHub, Discord e e-mail abrem serviços operados por terceiros. Informações enviadas a esses serviços são tratadas conforme seus termos e políticas de privacidade." },
        { id: "rights", title: "6. Seus direitos", content: "Conforme a legislação aplicável, incluindo LGPD e GDPR, você pode solicitar acesso, correção, exclusão, portabilidade ou informações sobre o tratamento de dados pessoais. Envie solicitações para privacy@phoxia.org." },
        { id: "changes", title: "7. Alterações e contato", content: "Mudanças relevantes atualizarão a data desta página e o repositório público phoxia-devkit. Privacidade: privacy@phoxia.org. Segurança: security@phoxia.org. Suporte geral: support@phoxia.org." },
      ],
    },
    terms: {
      title: "Termos de Uso",
      updated: "Última atualização: 14 de julho de 2026 · Minuta 1.0",
      status: "Minuta pendente de revisão jurídica",
      contents: "Conteúdo",
      sections: [
        { id: "scope", title: "1. Escopo", content: "Estes termos regem o acesso ao kit.phoxia.org e às informações públicas sobre o Phoxia DevKit. O software DevKit é distribuído separadamente sob a licença do seu repositório." },
        { id: "use", title: "2. Uso aceitável", content: "Você pode usar o site para finalidades lícitas. Você não pode tentar obter acesso não autorizado, interromper a disponibilidade, distribuir conteúdo malicioso ou personificar a Phoxia ou seus colaboradores." },
        { id: "license", title: "3. Licença open source", content: "O código-fonte do Phoxia DevKit é distribuído sob a GNU Affero General Public License v3.0, AGPLv3. Seus direitos de usar, estudar, modificar e distribuir o software são regidos pelo texto da licença no repositório phoxia-devkit." },
        { id: "content", title: "4. Conteúdo do site", content: "O conteúdo do site e da documentação é fornecido para fins informativos e pode mudar conforme o DevKit evolui. Instruções do projeto, RFCs aceitas, schemas, releases e arquivos de licença do repositório permanecem autoritativos." },
        { id: "third-parties", title: "5. Links de terceiros", content: "O site possui links para serviços externos, incluindo GitHub e Discord. A Phoxia não controla a disponibilidade, segurança, conteúdo, termos ou práticas de privacidade desses serviços." },
        { id: "disclaimer", title: "6. Isenção", content: "Na extensão permitida pela legislação aplicável, o site e o software são fornecidos conforme disponíveis e sem garantias além daquelas que não podem ser legalmente excluídas. Revise as mudanças geradas antes de aplicá-las a um repositório." },
        { id: "liability", title: "7. Limitação e legislação aplicável", content: "A responsabilidade é limitada na extensão permitida pela legislação aplicável. Estes termos são regidos pelas leis do Brasil, sem limitar direitos obrigatórios aplicáveis no local onde você vive." },
        { id: "changes", title: "8. Alterações e contato", content: "Mudanças relevantes atualizarão a data desta página e o repositório público phoxia-devkit. Questões jurídicas: legal@phoxia.org. Privacidade: privacy@phoxia.org. Suporte: support@phoxia.org." },
      ],
    },
  },
};
