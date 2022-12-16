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

