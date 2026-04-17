# 🛣️ Caminho Seguro - Boas Práticas do Projeto

## Workflow Recomendado

### 1. **Antes de fazer qualquer mudança:**
```bash
git status  # Ver o que mudou
git pull    # Atualizar (se tiver remoto)
```

### 2. **Durante o desenvolvimento:**
```bash
# Criar uma branch para cada feature
git checkout -b feature/nome-da-funcionalidade

# Fazer as alterações
# Testar tudo!

# Commits frequentes e descritivos
git add arquivo.py
git commit -m "Descrição clara do que foi feito"
```

### 3. **Ao finalizar a feature:**
```bash
# Voltar para master
git checkout master

# Atualizar
git pull

# Mergear a feature
git merge feature/nome-da-funcionalidade

# Deletar a branch
git branch -d feature/nome-da-funcionalidade
```

---

## 💾 Padrão de Commits

Use mensagens descritivas com este formato:

```
[TIPO] Mensagem breve (máx 50 caracteres)

Descrição mais detalhada se necessário.
- Detalhe 1
- Detalhe 2
```

**Tipos comuns:**
- `feat:` Nova funcionalidade
- `fix:` Correção de bug
- `refactor:` Reorganização do código
- `docs:` Documentação
- `test:` Testes
- `chore:` Tarefas administrativas

**Exemplo:**
```
feat: Adicionar busca de registros por placa

- Implementar função de busca
- Adicionar campo na interface
- Validar entrada do usuário
```

---

## 📦 Estrutura do Projeto (Seguir Sempre)

```
Projeto PYTHON/
├── main.py                 # Interface principal
├── dados_oficina.py        # Lógica da aplicação
├── rodar.sh               # Script de execução
├── Oficina.desktop        # Atalho da área de trabalho
├── registros.csv          # Dados (gerado automaticamente)
├── .git/                  # Repositório Git
├── .gitignore             # Arquivos ignorados
├── README.md              # Documentação
├── requirements.txt       # Dependências
└── ROADMAP.md             # Este arquivo (boas práticas)
```

---

## ⚠️ O que NÃO fazer

❌ Commitear arquivo CSV com dados sensíveis  
❌ Modificar múltiplas coisas em um único commit  
❌ Deixar código comentado ou quebrado  
❌ Fazer push sem testar  
❌ Alterar commits já enviados ao remoto  

---

## ✅ Checklist Antes de Commitear

- [ ] Código testado e funcionando
- [ ] Sem erros de sintaxe
- [ ] Sem código comentado desnecessário
- [ ] Mensagem de commit clara
- [ ] Apenas uma funcionalidade por commit (ideal)

---

## 🚀 Próximas Funcionalidades Sugeridas

1. **Backend com autenticação** (usuário/senha da oficina)
2. **Relatórios em PDF**
3. **Busca e filtros avançados**
4. **Edição de registros**
5. **Backup automático**
6. **Interface mobile/web**

Sempre que implementar algo novo, crie uma BRANCH!

---

**Desenvolvido com ❤️ para oficina do seu pai** 🔧
