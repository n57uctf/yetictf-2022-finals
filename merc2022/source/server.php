<?php
session_start();

$errors = array(); 

$_SESSION['db_string'] = @"host=postgres port=5432 dbname=merc user=user password=".getenv('DB_PASSWORD');

$db_connect = @pg_connect($_SESSION['db_string']);

function merc_id($name){
  return base64_encode($name);
}

if (isset($_POST['register'])) {
  $name = pg_escape_string($db_connect, $_POST['name']);
  $passwd = pg_escape_string($db_connect, $_POST['passwd']);
  $passwd_confirm = pg_escape_string($db_connect, $_POST['passwd_confirm']);

  if (empty($name)) { array_push($errors, "Name is required"); } else { 
      if (preg_match("/[<,>,\",',{,},$,|,:,*,?,\\,\/]/", $name)) {array_push($errors, "Forbidden symbols found!");}
     }
  if (empty($passwd)) { array_push($errors, "Password is required"); }
  if ($passwd != $passwd_confirm) {
	array_push($errors, "Passwords do not match");
  }

  if (count($errors) == 0) {
    $user_check_query = "SELECT * FROM merchants WHERE name='$name' LIMIT 1";
    $result = pg_query($db_connect, $user_check_query);
    $merc = pg_fetch_assoc($result);
  
    if ($merc) { 
      if ($merc['name'] === $name) {
        array_push($errors, "Merchant with that name already exists");
      }
    }
  }

  if (count($errors) == 0) {
  	$passwd = md5($passwd);
  	$merc_id = merc_id($name);
  	@pg_query($db_connect, "INSERT INTO merchants (name, passwd, merc_id) 
          VALUES('$name', '$passwd', '$merc_id')");
  	$_SESSION['name'] = $name;
  	header('location: cabinet.php');
    exit();
  }
}

if (isset($_POST['login'])) {
  $name = pg_escape_string($db_connect, $_POST['name']);
  $passwd = pg_escape_string($db_connect, $_POST['passwd']);

  if (empty($name)) {
  	array_push($errors, "Merchant ID is required");
  }
  if (empty($passwd)) {
  	array_push($errors, "Password is required");
  }

  if (count($errors) == 0) {
  	$passwd = md5($passwd);
  	$query = "SELECT * FROM merchants WHERE name='$name' AND passwd='$passwd'";
  	$results = pg_query($db_connect, $query);
    $merc = pg_fetch_assoc($results);
  	if (pg_num_rows($results) == 1) {
  	  $_SESSION['name'] = $name;
      $_SESSION['merc_id'] = $merc['merc_id'];
  	  header('location: cabinet.php');
      exit();
  	} else {
  		array_push($errors, "Something isn't right!");
  	}
  }
}

if (isset($_POST['request'])) {
  $dispatch = pg_escape_string($db_connect, $_POST['dispatch']);
  $destination = pg_escape_string($db_connect, $_POST['destination']);
  $note = pg_escape_string($db_connect, $_POST['note']);
  $name = pg_escape_string($db_connect, $_POST['name']);
  $merc_id = $_SESSION['merc_id'];

  if (empty($dispatch)) {
    array_push($errors, "Write a dispatch address!");
  }
  if (empty($destination)) {
    array_push($errors, "Write a destination address!");
  }
  if (empty($name)) {
    array_push($errors, "Select a driver!");
  }
  if ($dispatch === $destination) {
    array_push($errors, "Dispatch and destination is the same place!");
  }
  if (empty($note)) {
    $note = "None";
  }

  if (count($errors) == 0) {
    $timemark = date('h:i');
    $results = pg_query($db_connect, "SELECT driver_id FROM drivers WHERE name='$name' LIMIT 1");
    if (pg_num_rows($results) == 1) {
      $driver_id = pg_fetch_assoc($results)['driver_id'];
      @pg_query($db_connect, "INSERT INTO parsels (dispatch, destination, note, merc_id, driver_id) VALUES('$dispatch', '$destination', '$note', '$merc_id', '$driver_id')");
      @pg_query($db_connect, "INSERT INTO chat (sender_id, receiver_id, message, timemark, name) VALUES('$merc_id', '$driver_id', '$note', '$timemark', '$merc_id')");
      header('location: cabinet.php');
      exit();
    } else {
      array_push($errors,'No such driver');
    }
  }
}

if (isset($_POST['message'])) {
  $sender_id = pg_escape_string($db_connect, $_POST['sender_id']);
  $receiver_id = pg_escape_string($db_connect, $_POST['receiver_id']);
  $message = pg_escape_string($db_connect, $_POST['message']);
  $timemark = date('h:i');

  if ($sender_id=="" || empty($message || !isset($_SESSION['name']))) {
    array_push($errors, "No sender ID or empty message");
  }

  if (count($errors) == 0) {
    $name = pg_escape_string($db_connect, $_SESSION['name']);
    @pg_query($db_connect, "INSERT INTO chat (sender_id, receiver_id, message, timemark, name) 
          VALUES('$sender_id', '$receiver_id','$message', '$timemark', '$name')");
    header('location: chat.php');
  }
}

if (isset($_GET['track'])) {
  $track = pg_escape_string($db_connect, $_GET['track']);

  if (!empty($track)) {
      $_SESSION['merc_id'] = $track;
  }
}

function driver_id($name, $avatar){
  return md5($avatar.$name);
}

function image_process($image,$path){
    $png = imagecreatefrompng($image);
    $oldw = imagesx($png);
    $oldh = imagesy($png);
    $tmp = imagecreatetruecolor(100, 100);
    imagecopyresampled($tmp, $png, 0, 0, 0, 0, 100, 100, $oldw, $oldh);
    $png = $tmp;
    imagepng($png,$path);
    imagedestroy($png);
}

if (isset($_POST['driver'])) {
  $name = pg_escape_string($db_connect, $_POST['name']);
  $vehicle = pg_escape_string($db_connect, $_POST['vehicle']);
  $about = pg_escape_string($db_connect, $_POST['about']);
  $status = pg_escape_string($db_connect, $_POST['status']);

  if (empty($name)) {
    array_push($errors, "No name provided!");
  } else { 
      if (preg_match("/[<,>,\",',{,},$,|,:,*,?,\\,\/]/", $name)) {array_push($errors, "Forbidden symbols found!");}
    }
  if (empty($vehicle)) {
    array_push($errors, "Write vehicle info!");
  } else { 
      if (preg_match("/[<,>,\",',{,},$,|,:,*,?,\\,\/]/", $name)) {array_push($errors, "Forbidden symbols found!");}
    }
  if ($_FILES['avatar']['size'] > 900000 || $_FILES['license']['size'] > 900000) {
    array_push($errors, "File size limit is 900000 bytes!");
  }
  if ($_FILES['avatar']['error'] != UPLOAD_ERR_OK && !is_uploaded_file($_FILES['avatar']['tmp_name'])) {
    array_push($errors, "Upload your picture!");
  }
  if ($_FILES['license']['error'] != UPLOAD_ERR_OK && !is_uploaded_file($_FILES['license']['tmp_name'])) {
    array_push($errors, "Upload your Driver's license!");
  }
  if ($_FILES['avatar']['type'] != "image/png" || $_FILES['license']['type'] != "image/png") {
    array_push($errors, "Wrong file format!");
  }

  if (count($errors) == 0) {
    $driver_check = "SELECT * FROM drivers WHERE name='$name' LIMIT 1";
    $result = pg_query($db_connect, $driver_check);
    $driver = pg_fetch_assoc($result);

  
    if ($driver) { 
      if ($driver['name'] === $name) {
        array_push($errors, "Driver with that name already exists");
      }
    }
  }

  if (count($errors) == 0) {
    image_process($_FILES['avatar']['tmp_name'],'avatars/'.$name.'.png');
    move_uploaded_file($_FILES['license']['tmp_name'],'licenses/'.$name.'.png');
    $avatar = file_get_contents('avatars/'.$name.'.png');
    $license = file_get_contents('licenses/'.$name.'.png');
        $driver_id = driver_id($name,$avatar);
    @pg_query($db_connect, "INSERT INTO drivers (driver_id, name, vehicle, about, status) VALUES('$driver_id', '$name', '$vehicle', '$about', '$status')");
    $_SESSION['driver_id'] = $driver_id;
    $_SESSION['name'] = $name;
    $_SESSION['vehicle'] = $vehicle;
    $_SESSION['about'] = $about;
    $_SESSION['status'] = $status;
    header('location: application.php');
    exit();
  }
}

if (isset($_POST['application'])) {
  $driver_id = pg_escape_string($db_connect, $_POST['driver_id']);
  
  if (empty($driver_id)) {
    array_push($errors, "No Driver ID provided!");
  }

  if (count($errors) == 0) {
    $results = pg_query($db_connect, "SELECT * FROM drivers WHERE driver_id='$driver_id' LIMIT 1");
    if (pg_num_rows($results) == 1) {
    $driver_info = pg_fetch_assoc($results);
    $_SESSION['driver_id'] = $driver_id;
    $_SESSION['name'] = $driver_info['name'];
    $_SESSION['vehicle'] = $driver_info['vehicle'];
    $_SESSION['status'] = $driver_info['status'];
    header('location: application.php');
    exit();
    } else {
      array_push($errors, "No Driver found with such ID!");
    }
  }
}

if (isset($_GET['name'])) {
  $name = pg_escape_string($db_connect, $_GET['name']);

  if (!empty($name)) {
      $_SESSION['name'] = $name;
      header('location: advert.php');
      exit();
  }
}

if (isset($_POST['deliveries'])) {
  $driver_id = pg_escape_string($db_connect, $_POST['driver_id']);
  
  if (empty($driver_id)) {
    array_push($errors, "No Driver ID provided!");
  }

  if (count($errors) == 0) {
    $results = pg_query($db_connect, "SELECT * FROM parsels WHERE driver_id='$driver_id'");
    if (pg_num_rows($results) != 0) {
      $parsels = pg_fetch_all($results);
      foreach ($parsels as &$item) {
      echo $item['note']."\n";
      }
    }
  }
}

if (isset($_GET['logout'])) {
    session_destroy();
    header("location: ../index.php");
    exit();
}