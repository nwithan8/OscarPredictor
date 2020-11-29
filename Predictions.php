<!DOCTYPE html>

<html>    
    <head>
        <title>Oscar Predictions</title>
        <link rel="stylesheet" href="css/styles.css">
    </head>
    
    <body>
        <div class='container'>
            <div id="header-image"> <a href= "./index.html">
                <img src="img/header.png"> </a>
            </div>
            <h2> Oscar Predictions </h2>
            <div id="project-description">
                <p> Oscar Predictions Results</p><br><br>
            </div>
        </div>
    
    <?php
        
   file_put_contents("./movies_input.csv", "");
    file_put_contents("./predictions.csv", "");
    $name_list=array();
    $movieinput="Run_Time, Budget,Revenue, Gross_Rev, ROTTEN_SCORE,MPAA Rating (string),US_Release_month(int),US_Release_year(int),Peak_Box_Office,Director_Name,Director_Won_Best,Director_Nom,Director_Win, Actor_Name,Actor_Won_Best,Actor_Nom,Actor_Win,Actor2_Name,Actor2_Won_Best,Actor2_Nom,Actor2_Win,Actor3_Name,Actor3_Won_Best,Actor3_Nom,Actor3_Win ";
    for($i=0;$i<$_COOKIE["n"];$i++){
        $name_list[$i]=$_GET[strval($i+1)."mName"];
        $grossrev=$_GET[strval($i+1)."rev"]-$_GET[strval($i+1)."budget"];
        if (($_GET[strval($i+1)."dirWin"])>0){
            $dirwinB="TRUE";
        } else {
            $dirwinB="FALSE";
        }
        if (($_GET[strval($i+1)."actWin1"])>0){
            $actWin1B="TRUE";
        } else {
            $actWin1B="FALSE";
        }
        if (($_GET[strval($i+1)."actWin2"])>0){
            $actWin2B="TRUE";
        } else {
            $actWin2B="FALSE";
        }
        if (($_GET[strval($i+1)."actWin3"])>0){
            $actWin3B="TRUE";
        } else {
            $actWin3B="FALSE";
        }
        

        $movieinput.="\n".$_GET[strval($i+1)."rTime"].",".$_GET[strval($i+1)."budget"].",".$_GET[strval($i+1)."rev"].",".$grossrev.",".$_GET[strval($i+1)."rotten"].",".$_GET[strval($i+1)."mpaa"].",".$_GET[strval($i+1)."USMonth"].",".$_GET[strval($i+1)."release"].",".$_GET[strval($i+1)."peak"].",".$_GET[strval($i+1)."dir"].",".$dirwinB.",".$_GET[strval($i+1)."dirNom"].",".$_GET[strval($i+1)."dirWin"].",".$_GET[strval($i+1)."act1"].",".$actWin1B.",".$_GET[strval($i+1)."actNom1"].",".$_GET[strval($i+1)."actWin1"].",".$_GET[strval($i+1)."act2"].",".$actWin2B.",".$_GET[strval($i+1)."actNom2"].",".$_GET[strval($i+1)."actWin2"].",".$_GET[strval($i+1)."act3"].",".$actWin3B.",".$_GET[strval($i+1)."actNom3"].",".$_GET[strval($i+1)."actWin3"];
        /*
        $movie_name[$i]=$_GET[strval($i+1)."mName"];
        $movie_array=array();
        $grossrev=$_GET[strval($i+1)."rev"]-$_GET[strval($i+1)."budget"];
        array_push($movie_array,$_GET[strval($i+1)."rTime"],$_GET[strval($i+1)."budget"],$_GET[strval($i+1)."rev"],$grossrev,$_GET[strval($i+1)."rotten"],$_GET[strval($i+1)."mpaa"],$_GET[strval($i+1)."USMonth"],$_GET[strval($i+1)."release"],$_GET[strval($i+1)."peak"],$_GET[strval($i+1)."dir"],$_GET[strval($i+1)."dirNom"],$_GET[strval($i+1)."dirWin"],$_GET[strval($i+1)."act1"],$_GET[strval($i+1)."actNom1"],$_GET[strval($i+1)."actWin1"],$_GET[strval($i+1)."act2"],$_GET[strval($i+1)."actNom2"],$_GET[strval($i+1)."actWin2"],$_GET[strval($i+1)."act3"],$_GET[strval($i+1)."actNom3"],$_GET[strval($i+1)."actWin3"]);
        $movie_list[$i]=$movie_array;
        */
   }
  
       $fp=fopen("movies_input.csv","w");
    
    fwrite($fp,$movieinput);
    fclose($fp);
    exec("sudo python3.8 oscars_classifier.py 2>&1",$output);
     


    
    $results=explode(",",file_get_contents("predictions.csv"));
    echo"<br>";
    
    for($i=0;$i<count($name_list);$i++){
        $answers=$results[$i]*100;
        echo "<h3>$name_list[$i] <br>$answers% </h3>";
    }
    

    
    ?>
    </body>
</html>