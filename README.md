# Sistema de Gerenciamento de Oficina

Um aplicativo simples e intuitivo para gerenciar registros de serviços em uma oficina mecânica.

## Características

✅ Interface gráfica amigável com tkinter  
✅ Registro de dados básicos do carro (marca, modelo, ano, placa)  
✅ Seleção de tipos de serviço predefinidos  
✅ Armazenamento em arquivo CSV  
✅ Visualização de todos os registros  
✅ Descrição adicional opcional para cada serviço  

## Requisitos

- Python 3.7 ou superior
- tkinter (geralmente vem instalado com Python)

## Como Instalar

1. Clone ou baixe este projeto
2. Navegue até a pasta do projeto
3. Não há dependências externas, apenas Python puro!

## Como Usar

1. Execute o programa:
```bash
python main.py
```

2. A interface será aberta com um formulário para preenchimento
3. Preencha os dados:
   - **Marca**: Marca do carro (ex: Toyota, Ford)
   - **Modelo**: Modelo do carro (ex: Corolla, Fiesta)
   - **Ano**: Ano de fabricação do carro
   - **Placa**: Placa do veículo
   - **Tipo de Serviço**: Selecione na lista
   - **Descrição**: Adicione detalhes extras (opcional)

4. Clique em **"Salvar Registro"** para armazenar os dados
5. Use **"Ver Registros"** para visualizar o histórico
6. Use **"Limpar"** para limpar o formulário

## Estrutura dos Arquivos

```
Projeto PYTHON/
├── main.py              # Interface gráfica principal
├── dados_oficina.py     # Lógica e gerenciamento de dados
├── registros.csv        # Arquivo com os registros (criado automaticamente)
└── README.md            # Este arquivo
```

## Tipos de Serviço Disponíveis

- Troca de Óleo
- Troca de Filtro de Ar
- Balanceamento de Pneus
- Alinhamento
- Troca de Pneus
- Revisão Geral
- Reparo do Motor
- Reparo de Freios
- Ar Condicionado
- Elétrica
- Suspensão
- Outro

## Atualizações Futuras

Ideias para melhorias:
- [ ] Adicionar campo de cliente/proprietário
- [ ] Incluir valores/preços dos serviços
- [ ] Gerar relatórios/estatísticas
- [ ] Buscar registros por placa
- [ ] Editar registros existentes
- [ ] Backup automático de dados
- [ ] Interface para adicionar novos tipos de serviço

## Suporte

Se tiver dúvidas ou sugestões, sinta-se à vontade para melhorar o projeto!

---
**Desenvolvido para facilitar o gerenciamento da oficina** 🔧
