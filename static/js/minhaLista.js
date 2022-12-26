var formaConsulta = document.getElementById("formaConsulta").innerHTML;
var anoMin = document.getElementById("anoMin").innerHTML;
var anoMax = document.getElementById("anoMax").innerHTML;
var duracaoMin = document.getElementById("duracaoMin").innerHTML;
var duracaoMax = document.getElementById("duracaoMax").innerHTML;
var notaMin = document.getElementById("notaMin").innerHTML;
var notaMax = document.getElementById("notaMax").innerHTML;
var genero = document.getElementById("genero-pesquisa").innerHTML;


// Função que adiciona o filme à Minha Lista
function adicionarMinhaLista() {

    idFilme = document.getElementsByClassName('hide id-filme')[0].id

    window.location.href = "/salvar/" + idFilme

}


// Função que remove o filme da Minha Lista
function removerMinhaLista() {

   idFilme = document.getElementsByClassName('hide id-filme')[0].id

   window.location.href = "/remover/" + idFilme

}


// Função que abre o formulário de consulta
function abrirForm() {
  document.getElementById("consulta-minha-lista").style.display = "block";
}

// Função que fecha o formulário de consulta
function fecharForm() {
  document.getElementById("consulta-minha-lista").style.display = "none";
}


// Função que retorna à pesquisa realizada com os mesmos parâmetros
function retornarPesquisa() {

    window.location.href = "/filmes/" + formaConsulta + "/" + anoMin + "/" + anoMax + "/" + duracaoMin + "/" + duracaoMax + "/" + notaMin + "/" + notaMax + "/" + genero

}


// Botão que retorna à pagina da lista de filmes sem nenhum parâmetro
function retornarFilmes() {

    window.location.href = "/filmes"

}
