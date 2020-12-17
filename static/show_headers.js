
import * as mysql from 'mysql';

businesses = [
    {
      'id':'1',
      'name':'Akko Sweets',
      'email':'akkosweets@gmail.com',
      'phone':'0528529817',
      'business type':'Sweets',
      'profile image':'https://media.timeout.com/images/103700330/750/422/image.jpg',
      'description':'Local sweets from akko'
    },
    {
      'id':'2',
      'name':'The Fat Duck',
      'email':'thefatduck@gmail.com',
      'phone':'0524971850',
      'business type':'British Cuisine',
      'profile image':'https://www.thefatduckgroup.com/wp-content/uploads/2018/10/home-square-3.jpg',
      'description':'British cuisine dishes by Heston Blumenthal'
    },
    {
      'id':'3',
      'name':'PETRUS',
      'email':'petrus@gmail.com',
      'phone':'0549718064',
      'business type':'French Cuisine',
      'profile image':'https://static01.nyt.com/images/2019/12/13/dining/mc-beef-wellington/mc-beef-wellington-articleLarge.jpg',
      'description':'French cuisine dishes by Gordon Ramsey'
    },
    {
      'id':'4',
      'name':'PETRUS',
      'email':'petrus@gmail.com',
      'phone':'0549718064',
      'business type':'French Cuisine',
      'profile image':'https://static01.nyt.com/images/2019/12/13/dining/mc-beef-wellington/mc-beef-wellington-articleLarge.jpg',
      'description':'French cuisine dishes by Gordon Ramsey'
    }
  ]

 

  function show_businesses_data(){
    var con = mysql.createConnection({
      host: "localhost",
      user: "root",
      password: "",
      database: "business_db"
    });
    
    con.connect(function(err) {
      if (err) throw err;
      con.query("SELECT * FROM owners", function (err, result, fields) {
        if (err) throw err;
        console.log(result);
        console.log(result);
      });
    });

    businesses.forEach(business => {
      var businesses_row = document.getElementById('businesses_row');
      businesses_row.innerHTML +=
        '<div class="col-md-4">' +
          '<h2>' + business["name"] + '</h2>' +
          '<img src="' + business["profile image"] + '" alt="' + business["name"] + '" style="width: 90%"></img>' +
          '<p>' + business["business type"] + '</p>' +
          '<p>' + business["description"] + '</p>' +
          '<p>' + business["phone"] + '</p>' +
          '<p>' + business["email"] + '</p>' +
        '</div>';
    });
  }
