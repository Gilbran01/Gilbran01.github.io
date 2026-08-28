# Achadinhos - site automatico de afiliados

Site estatico que se atualiza sozinho todo dia via GitHub Actions (nao
depende do seu PC estar ligado). Publica produtos com seus links de
afiliado da Shopee/Mercado Livre e busca ideias de produto automaticamente
na API publica do Mercado Livre.

## O que roda sozinho
- Todo dia as 06:00 (horario de Brasilia) o GitHub Actions regenera o site.
- Assim que voce editar `data/products.csv` e enviar (push), o site
  republica sozinho.
- O GitHub Pages fica servindo o conteudo da pasta `docs/` automaticamente.
- O script tambem tenta buscar ideias de produto na API publica do Mercado
  Livre (`data/ml_ideas.json`), mas isso e "melhor esforco": o Mercado
  Livre restringiu essa busca e hoje costuma bloquear com erro 403 sem
  um aplicativo registrado (o que exigiria mais um cadastro manual). Se
  falhar, nao quebra nada -- o site continua sendo gerado normalmente.

## O que so voce pode fazer (nao da pra automatizar)
Gerar o link de afiliado exige estar logado no painel da Shopee/Mercado
Livre -- isso e um login humano, nenhum script pode fazer por voce.
O fluxo manual, quando quiser adicionar um produto novo, e:
1. Achar o produto (pode olhar `data/ml_ideas.json`, que e atualizado
   sozinho todo dia com sugestoes).
2. Gerar o link de afiliado no painel da Shopee ou do Mercado Livre.
3. Adicionar uma linha em `data/products.csv` com esse link.
4. Dar `git push` (ou editar direto pelo site do GitHub, sem precisar do PC).

Isso e literalmente o unico passo manual do sistema inteiro.

## Configuracao inicial (unica vez, leva uns 20-30 min)

1. Crie um repositorio novo no GitHub (pode ser publico).
2. Suba esta pasta para o repositorio:
   ```
   git init
   git add .
   git commit -m "Site inicial de achadinhos"
   git branch -M main
   git remote add origin https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git
   git push -u origin main
   ```
3. No GitHub, va em **Settings > Pages** e configure:
   - Source: `Deploy from a branch`
   - Branch: `main`, pasta `/docs`
4. Edite `config.json`:
   - `site_url`: coloque a URL que o GitHub Pages vai te dar
     (algo como `https://SEU-USUARIO.github.io/SEU-REPOSITORIO`).
5. Va em **Settings > Actions > General** e confirme que
   "Workflow permissions" esta como **Read and write permissions**
   (necessario para o robo poder commitar sozinho).
6. Adicione seus produtos reais em `data/products.csv`, com os links
   de afiliado da Shopee/Mercado Livre, e de um `git push`.
7. (Opcional, mas recomendado) Cadastre o site no Google Search Console
   e envie `https://SEU-USUARIO.github.io/SEU-REPOSITORIO/sitemap.xml`
   para acelerar a indexacao.

## Expectativa realista de tempo
- O sistema fica todo automatizado a partir de hoje.
- Indexacao no Google normalmente leva de alguns dias a poucas semanas.
- Vendas dependem de trafego, entao o inicio e mais lento -- isso nao
  substitui renda imediata, e uma base que cresce com manutencao minima
  (adicionar produtos de vez em quando).
