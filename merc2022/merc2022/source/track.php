Express parsel status check:
<p></p>
<?if (isset($_SESSION['merc_id'])):?>
<?php 
  $merc_id = $_SESSION['merc_id'];
  $results = pg_query(pg_connect($_SESSION['db_string']), "SELECT * FROM parsels WHERE merc_id='$merc_id'");
  if (pg_num_rows($results) != 0) :
    $parsels = pg_fetch_all($results); 
?><div style="overflow:auto;height:340px">
  <table>
    <tr style="background-color:  lightgrey;">
      <td style="width: 5%"><strong>N</strong></td>
      <td style="width: 20%"><strong>Dispatch</strong></td>
      <td style="width: 20%"><strong>Destination</strong></td>
      <td><strong>Comments</strong></td>
      <td style="width: 15%"><strong>Driver</strong></td>
    </tr>
<?php $c = 1; foreach ($parsels as &$item) :?>
    <tr>
<?php echo '<td>'.$c.'</td>'; $counter=0; foreach ($item as &$pos) : if ($counter!=0 && $counter!=4) : if ($counter==5) : $results = pg_query(pg_connect($_SESSION['db_string']), "SELECT name FROM drivers WHERE driver_id='$pos' LIMIT 1"); if ($results !=0 ) : echo "<td>".pg_fetch_assoc($results)['name']."</td>"; endif; else : echo "<td>".$pos."</td>"; endif; endif; ++$counter; endforeach; $c++
?>
    </tr>
<?php endforeach ?>
  </table>
</div>
<?php else : ?>
    You don't have any parsels!
<?php endif ?>
<?php endif;?>