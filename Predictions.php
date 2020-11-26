<html>
    <header>
        <title>
        </title>
    </header>
<body>
    <h1>Predictions Results</h1>
    
    <?php
   
    $name_list=array();
    $movie_list=array();
    for($i=0;$i<$_COOKIE["n"];$i++){
        $movie_name[$i]=$_GET[strval($i+1)."mName"];
        $movie_array=array();
        $grossrev=$_GET[strval($i+1)."rev"]-$_GET[strval($i+1)."budget"];
        array_push($movie_array,$_GET[strval($i+1)."rTime"],$_GET[strval($i+1)."budget"],$_GET[strval($i+1)."rev"],$grossrev,$_GET[strval($i+1)."rotten"],$_GET[strval($i+1)."mpaa"],$_GET[strval($i+1)."USMonth"],$_GET[strval($i+1)."release"],$_GET[strval($i+1)."peak"],$_GET[strval($i+1)."dir"],$_GET[strval($i+1)."dirNom"],$_GET[strval($i+1)."dirWin"],$_GET[strval($i+1)."act1"],$_GET[strval($i+1)."actNom1"],$_GET[strval($i+1)."actWin1"],$_GET[strval($i+1)."act2"],$_GET[strval($i+1)."actNom2"],$_GET[strval($i+1)."actWin2"],$_GET[strval($i+1)."act3"],$_GET[strval($i+1)."actNom3"],$_GET[strval($i+1)."actWin3"]);
        $movie_list[$i]=$movie_array;
   }
    $Predictions=array();
exec('python "./models/oscars_classifier.py" "'.$movie_list.'"', $output, $Predictions);
    for($i=0;$i<count(movie_list);$i++){
        print_r($Predictions);
    }
    

    
    ?>
    </body>
</html>