<?php
header('Content-Type: text/html; charset=utf-8');
// Connexion et sélection de la base

require('includes/acces.php');

//echo 'Connected successfully';
mysql_select_db('paglalzs_echopa') or die('Impossible de sélectionner la base de données');

if(isset($_GET['id']) && !empty($_GET['id'])){
	$id= preg_replace('/[^-a-zA-Z0-9_]/', '', $_GET['id']);

	// Exécution des requêtes SQL
	$query = "SELECT * FROM patents WHERE pShortID LIKE '".$id."'";
	$result = mysql_query($query) or die('Échec de la requête : ' . mysql_error());
	//echo $query;
	// Affichage des résultats en HTML
	if(empty($row)){
		echo("Rien trouvé, retourner au <a href='patents.php'>départ</a>.");
	}
	while ($row = mysql_fetch_array($result, MYSQL_NUM)) {
		echo("<p><h3><u> ID: <a href='http://www.google.com/patents/");
		echo($row[3]);
		echo("' target='_new'>");
		echo($row[3]);
		echo(" sur Google</a> <b>");
		echo($row[1]);
		echo("</b> by <i>");
		echo($row[5]);
		echo("</i></u></h3><p>Etat de l'art antérieur<ul>");
		
		$backward = explode(", ", $row[7]);
		foreach ($backward as $key => $value) {
		    echo "<li><a href='patents.php?id=".$value."'>".$value."</a> ou sur <a href='https://www.google.com/patents/".$value."' target='_new'>Google</a></li>\n";
		}
		echo("</ul>");

		;

		echo("</ul><p>Etat de l'art postérieur<ul>");
		
		$backward = explode(", ", $row[8]);
		foreach ($backward as $key => $value) {
		    echo "<li><a href='patents.php?id=".$value."'>".$value."</a> ou sur <a href='https://www.google.com/patents/".$value."' target='_new'>Google</a></li>\n";
		}
		echo("</ul>");

		
		echo($row[6]);
		echo("<p/>");
	}
	
}else{
	// Exécution des requêtes SQL
	$query = 'SELECT * FROM patents';
	$result = mysql_query($query) or die('Échec de la requête : ' . mysql_error());
	
	// Affichage des résultats en HTML
	
	
	while ($row = mysql_fetch_array($result, MYSQL_NUM)) {
		echo("<p><u> ID: <a href='patents.php?id=");
		echo($row[3]);
		echo("'>");
		echo($row[3]);
		echo("</a> <b>");
		echo($row[1]);
		echo("</b> by <i>");
		echo($row[5]);
		echo("</i></u><br>");
		echo("<p/>");
	}

}






// Libération des résultats
mysql_free_result($result);

// Fermeture de la connexion
mysql_close($link);
?>
