const listaPesquisa = document.getElementById('lista-pesquisa');
const gradeResultado = document.getElementsByClassName('grade-resultado')[0];
const pesquisaFilme = document.getElementById('pesquisa-filme');


// Adicionando evento de click que esconde a lista de pesquisa
window.addEventListener('click', (event) => {
    if(event.target.className != "formulario"){
        listaPesquisa.classList.add('hide-lista-pesquisa');
    }
});


// Function que pega o termo pesquisado, e retorna a lista de correspondências
function jsAcharFilmes() {
    let termoPesquisado = (pesquisaFilme.value).trim();
    if(termoPesquisado.length > 0){
        listaPesquisa.classList.remove('hide-lista-pesquisa');
        jsCarregarFilmes(termoPesquisado);
    } else {
        listaPesquisa.classList.add('hide-lista-pesquisa');
    }
}


// Function que carrega os filmes da API
async function jsCarregarFilmes(termoPesquisado) {
    const link = `https://omdbapi.com/?s=${termoPesquisado}&page=1&apikey=b0202a42`;
    const resposta = await fetch(`${link}`);
    const dados = await resposta.json();
    if(dados.Response == "True") jsMostrarListaFilmes(dados.Search);
}


// Function que gera a lista de pesquisa em uma div
function jsMostrarListaFilmes(titulos) {
    listaPesquisa.innerHTML = "";
    for(let n = 0; n < titulos.length; n++){
        let elementoListaPesquisa = document.createElement('div');
        elementoListaPesquisa.dataset.id = titulos[n].imdbID;
        elementoListaPesquisa.classList.add('lista-pesquisa-item');
        if(titulos[n].Poster != "N/A")
            filmePoster = titulos[n].Poster;
        else 
            filmePoster = "/static/image/sem_imagem.gif";

        elementoListaPesquisa.innerHTML = `
        <div class = "item-pesquisa-poster">
            <img src="${filmePoster}">
        </div>
        <div class="item-pesquisa-info">
            <h3>${titulos[n].Title}</h3>
            <p>${titulos[n].Year}</p>
        </div>
        `;
        listaPesquisa.appendChild(elementoListaPesquisa);
    }
    jsCarregarInfosFilme();
}


async function jsMostrarInfosFilme(infos) {

    const idFilme = infos.imdbID
    const idChaveFilme = infos.imdbID + 'key'
    const chaveMinhaListaBotao = infos.imdbID + 'watchlistBtn'
    const chaveBotaoRemover = infos.imdbID + 'removeBtn'

    gradeResultado.id = idChaveFilme + 'Grade';

    removerBotoes(idChaveFilme)
}


// Function que que carrega as informações do filme, para serem retornadas ao HTML em outra function
function jsCarregarInfosFilme() {
    const listaPesquisaFilmes = listaPesquisa.querySelectorAll('.lista-pesquisa-item');
    listaPesquisaFilmes.forEach(titulo => {
        titulo.addEventListener('click', async () => {
            listaPesquisa.classList.add('hide-lista-pesquisa');
            pesquisaFilme.value = "";
            const result = await fetch(`http://www.omdbapi.com/?i=${titulo.dataset.id}&apikey=b0202a42`);
            const filmeInfos = await result.json();

            jsMostrarInfosFilme(filmeInfos)

            idFilme = filmeInfos.imdbID
            console.log(idFilme)
            window.location.href = '/resultado/' + idFilme
        });
    });
}
