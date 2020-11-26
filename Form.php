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
            <h2> Oscar Nominee Submission Form </h2>
            <div id="project-description">
                <p> Enter the Oscar Movie Nominee</p><br><br>
            </div>
        </div>

<form action="./Predictions.php">
    
<?php
    
    $_SESSION['num']=$_GET['num'];
    setcookie("n",$_GET["num"], time() + (86400 * 30), "/"); 
    for($i=1;$i<=$_SESSION['num'];$i++){
    
    echo"<p class ='formtitle'><br><b>Movie $i Nomination Information</b></p>";
  
    echo'<label for="'.$i.'mName"><b>Movie Name:</b></label><br>
    <input type="text" id="'.$i.'mName" name="'.$i.'mName"><br>
  <label for="rTime">Run Time:</label><br>
    <input type="number" id="'.$i.'rTime" name="'.$i.'rTime"><br>
    <label for="budget">Budget:</label><br>
    <input type="number" id="'.$i.'budget" name="'.$i.'budget"><br>
    <label for="rev">Revenue:</label><br>
     <input type="number" id="'.$i.'rev" name="'.$i.'rev"><br>
     <label for="rotten">Rotten Tomato Score:</label><br>
     <input type="number" id="'.$i.'rotten" name="'.$i.'rotten"><br>
    <label for ="mpaa">MPAA Rating</label><br>
    <select id="'.$i.'mpaa" name="'.$i.'mpaa">
        <option value="G">G</option>
        <option value="PG">PG</option>
        <option value="PG-13">PG-13</option>
        <option value="R">R</option>
    </select><br>
    <label for="USMonth"> US Release Month:</label><br>
    <select id="'.$i.'USMonth" name="'.$i.'USMonth">
        <option value=1>January</option>
        <option value=2>February</option>
        <option value=3>March</option>
        <option value=4>April</option>
        <option value=5>May</option>
        <option value=6>June</option>
        <option value=7>July</option>
        <option value=8>August</option>
        <option value=9>September</option>
        <option value=10>October</option>
        <option value=11>November</option>
        <option value=12>December</option>
    </select><br>
    <label for="release">Release Year:</label><br>
    <input type="number" id="'.$i.'release" name="'.$i.'release"><br>
    <label for ="peak">Peak Box Office Ranking</label><br>
    <input type="number" id="'.$i.'peak" name="'.$i.'peak"><br><br>
   
    <label for="dir"><b>Director Name:</b></label><br>
    <input type="text" id="'.$i.'dir" name="'.$i.'dir"><br>
    <label for="dirNom">Director Nomination:</label><br>
    <input type="number" id="'.$i.'dirNom" name="'.$i.'dirNom"><br>
    <label for="dirWin">Director Wins:</label><br>
    <input type="number" id="'.$i.'dirWin" name="'.$i.'dirWin"><br>
   
    <label for="act1"><b>Actor/Actress Name:</b></label><br>
    <input type="text" id="'.$i.'act1" name="'.$i.'act1"><br>
    <label for="actNom1">Actor/Actress Nomination:</label><br>
    <input type="number" id="'.$i.'actNom1" name="'.$i.'actNom1"><br>
    <label for="actWin1">Actor/Actress Wins:</label><br>
    <input type="number" id="'.$i.'actWin1" name="'.$i.'actWin1"><br><br>
    <label for="act2"><b>Actor/Actress Name:</b></label><br>
    <input type="'.$i.'text" id="act2" name='.$i.'"act2"><br>
    <label for="actNom2">Actor/Actress Nomination:</label><br>
    <input type="number" id="'.$i.'actNom2" name="'.$i.'actNom2"><br>
    <label for="actWin2">Actor/Actress Wins:</label><br>
    <input type="number" id="'.$i.'actWin2" name="'.$i.'actWin2"><br><br>
    <label for="act3"><b>Actor/Actress Name:</b></label><br>
    <input type="text" id="'.$i.'act3" name="'.$i.'act3"><br>
    <label for="actNom3">Actor/Actress Nomination:</label><br>
    <input type="number" id="'.$i.'actNom3" name="'.$i.'actNom3"><br>
    <label for="actWin3">Actor/Actress Wins:</label><br>
    <input type="number" id="'.$i.'actWin3" name="'.$i.'actWin3"><br><br>
    </ul>';
    }?>
    
    <input type="submit" value="Submit Predictions">

    <button type="submit" formaction="./index.html">Change # Nominations</button>
</form>
        
    </body>
    
</html>