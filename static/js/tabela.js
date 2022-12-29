var $table = document.getElementById("table-minha-lista"),

// numero de linhas por página
$n = 5,

// numero de linhas da tabela
$rowCount = $table.rows.length
,
// obter a tag da primeira célula na primeira linha
$firstRow = $table.rows[0].firstElementChild.tagName,
// booleano var para checar se tabela possui cabeçalho
$hasHead = ($firstRow === "TH"),
// um array para segurar cada linha
$tr = [],
// contadores em loop, que começa a contar da linha 2 se a primeira linha possui tag de cabeçalho
$i,$ii,$j = ($hasHead)?1:0,
// segurar a primeira linha se ela possui (<TH>) tag e não segurar se for (<TD>) tag
$th = ($hasHead?$table.rows[(0)].outerHTML:"");
// contar o número de páginas
var $pageCount = Math.ceil($rowCount / $n);
// se existir apenas uma página, então que a paginação não exista
if ($pageCount > 1) {
  // atribuir o outHTML de cada linha (tag name e innerHTML) ao array
  for ($i = $j,$ii = 0; $i < $rowCount; $i++, $ii++)
    $tr[$ii] = $table.rows[$i].outerHTML;
  // criar uma div block para conter os botões
  $table.insertAdjacentHTML("afterend","<div id='buttons'></div");
  // o primeiro sort, a página padrão é a primeira
  sort(1);
}

// ($p) é a página selecionada. Irá ser gerada quando o usuário clicar no botão
function sort($p) {
  var $rows = $th,$s = (($n * $p)-$n);
  for ($i = $s; $i < ($s+$n) && $i < $tr.length; $i++)
    $rows += $tr[$i];

  // agora a tabela possui um grupo processado de linhas ..
  $table.innerHTML = $rows;
  // criando os botões de paginação
  document.getElementById("buttons").innerHTML = pageButtons($pageCount,$p);
  // CSS stuff
  document.getElementById("id"+$p).setAttribute("class","chart");

  // Setando para que seja realçado a pagína atual da paginação
  document.getElementById("id"+$p).style.color = "#fdbf1b";
}


// ($pCount) : número de páginas, ($cur) : página atual, a que foi selecionada ..
function pageButtons($pCount,$cur) {
  /* essa variável vai desabilitar o botão de "ANTERIOR" na primeira página
     e o botão de  "PRÓXIMO" na última página */
  var $prevDis = ($cur == 1)?"disabled":"",
    $nextDis = ($cur == $pCount)?"disabled":"",
    /* esses ($buttons) vão criar cada butão e setar os atributos do onclick
    ** para a função "sort" com o número ($p) ...
    */
    $buttons = "<input class='chart' type='button' value='&lt;&lt; Anterior' onclick='sort("+($cur - 1)+")' "+$prevDis+">";
  for ($i=1; $i<=$pCount;$i++)
    $buttons += "<input  class='chart' type='button' id='id"+$i+"'value='"+$i+"' onclick='sort("+$i+")'>";
  $buttons += "<input class='chart' type='button' value='Próximo &gt;&gt;' onclick='sort("+($cur + 1)+")' "+$nextDis+">";
  return $buttons;
}

Footer
