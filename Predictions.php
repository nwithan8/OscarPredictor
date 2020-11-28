<!DOCTYPE html>

<html>    
    <head>
        <title>Oscar Predictions</title>
        <link rel="stylesheet" href="css/styles.css">
    </head>
    
    <body>
        <div class='container'>
            <div id="header-image"> 
                <img src="img/header.png"> 
            </div>
            <h2> Oscar Predictions </h2>
            <div id="project-description">
                <p> Oscar Predictions Results</p><br><br>
            </div>
        </div>
    
    <?php
   file_put_contents("./models/movies_input.csv", "");
    file_put_contents("./models/predictions.csv", "");
    $name_list=array();
    $movieinput;
    for($i=0;$i<$_COOKIE["n"];$i++){
    $name_list[$i]=$_GET[strval($i+1)."mName"];
    $grossrev=$_GET[strval($i+1)."rev"]-$_GET[strval($i+1)."budget"];
    $moviesinput+=$_GET[strval($i+1)."rTime"].",".$_GET[strval($i+1)."budget"].",".$_GET[strval($i+1)."rev"].",".$grossrev.",".$_GET[strval($i+1)."rotten"].",".$_GET[strval($i+1)."mpaa"].",".$_GET[strval($i+1)."USMonth"].",".$_GET[strval($i+1)."release"].",".$_GET[strval($i+1)."peak"].",".$_GET[strval($i+1)."dir"].",".$_GET[strval($i+1)."dirNom"].",".$_GET[strval($i+1)."dirWin"].",".$_GET[strval($i+1)."act1"].",".$_GET[strval($i+1)."actNom1"].",".$_GET[strval($i+1)."actWin1"].",".$_GET[strval($i+1)."act2"].",".$_GET[strval($i+1)."actNom2"].",".$_GET[strval($i+1)."actWin2"].",".$_GET[strval($i+1)."act3"].",".$_GET[strval($i+1)."actNom3"].",".$_GET[strval($i+1)."actWin3"];
        /*
        $movie_name[$i]=$_GET[strval($i+1)."mName"];
        $movie_array=array();
        $grossrev=$_GET[strval($i+1)."rev"]-$_GET[strval($i+1)."budget"];
        array_push($movie_array,$_GET[strval($i+1)."rTime"],$_GET[strval($i+1)."budget"],$_GET[strval($i+1)."rev"],$grossrev,$_GET[strval($i+1)."rotten"],$_GET[strval($i+1)."mpaa"],$_GET[strval($i+1)."USMonth"],$_GET[strval($i+1)."release"],$_GET[strval($i+1)."peak"],$_GET[strval($i+1)."dir"],$_GET[strval($i+1)."dirNom"],$_GET[strval($i+1)."dirWin"],$_GET[strval($i+1)."act1"],$_GET[strval($i+1)."actNom1"],$_GET[strval($i+1)."actWin1"],$_GET[strval($i+1)."act2"],$_GET[strval($i+1)."actNom2"],$_GET[strval($i+1)."actWin2"],$_GET[strval($i+1)."act3"],$_GET[strval($i+1)."actNom3"],$_GET[strval($i+1)."actWin3"]);
        $movie_list[$i]=$movie_array;
        */
   }
    $movie_file=fopen("./models/movies_input.csv","w");
    fwrite($movie_file,$moviesinput);
    
exec('python ./models/oscars_classifier.py movies_input.csv');
    fclose($movie_file);
    $results=explode("/\n|,/",file-get_Contents("predictions.csv"));
        
    for($i=0;$i<count($name_list);$i++){
        echo "<br><h3>$name_list[i] $results[i] </h3>";
    }
    

    
    ?>
    </body>
</html>