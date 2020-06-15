/* Add your Application JavaScript */

Vue.component('app-header', {
    template: `
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary fixed-top">
    <img src= "https://i.pinimg.com/736x/13/49/00/134900a338da0be769dd47e4719e633d.jpg" width= "30" 
    height= "30" alt="Photo of a camera drawing" >
      <a class="navbar-brand" href="#">Photogram</a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
    
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav mr-auto">
        </ul>
      </div>
      
        <ul class="navbar-nav">
            <li class="nav-item active">
                <router-link class="nav-link" to="/">Home <span class="sr-only">(current)</span></router-link>
            </li>
            <li class="nav-item active">
              <router-link class="nav-link" to="/explore">Explore</router-link>
            </li>
            <li class="nav-item active">
              <router-link class="nav-link" :to="{name: 'users', params: {user_id: cu_id}}">My Profile</router-link>
            </li>
            <li v-if="auth" class="nav-item active">
              <router-link class="nav-link" to="/logout">Logout</router-link>
            </li>
            <li v-else class="nav-item">
              <router-link class="nav-link active" to="/login">Login</router-link>
            </li>
        </ul>
    </nav>
    `,
    data: function(){
        return {
            auth: localStorage.hasOwnProperty("current_user"),
            cu_id: localStorage.hasOwnProperty("current_user") ? JSON.parse(localStorage.current_user).id : null
        }
    }
});

Vue.component('app-footer', {
    template: `
    <footer>
        <div class="container">
            
        </div>
    </footer>
    `
});

const Home = Vue.component('home', {
   template: `
    <div class="row landing-container">
    <div class="left-component">
            <img class= "homePagePhoto" src= "data:image/jpeg;base64,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"
            alt = "Image of Bridge" height= "400" width= "500">
        </div>
        <div class="right-component">
        <img src= "https://i.pinimg.com/736x/13/49/00/134900a338da0be769dd47e4719e633d.jpg" width= "30" 
        height= "30" alt="Photo of a camera drawing" >
        <h2 class="styleHeading">Photogram</h2><br>
              <p class="card-text">Share photos of your favourite moments with friends, family and the world.</p><br>
                  <router-link class="btn btn-success col-md-5" to="/register">Register</router-link>
                  <router-link class="btn btn-primary col-md-5" to="/login">Login</router-link>
              </div>
    </div>
   `,
    data: function() {
       return {}
    }
});

const Login = Vue.component('login',{
  template:`
  <div id ="login">
  <div class="container">
  <form id="LoginForm" @submit.prevent="LoginForm" method="POST" enctype="multipart/form-data">
  <div id="login-row" class="row justify-content-center align-items-center">
                <div id="login-column" class="col-md-6">
                    <div id="login-box" class="col-md-12">
    <h3 class="text-center text-info">Login</h3>
    <div class="form-group">
        <label for="username" class="text-info">Username</label><br>
        <input type="text" name="username" id="username" class="form-control">
      </div>
    <div class="form-group">
      <label for="password" class="text-info">Password</label><br>
      <input type="text" name="password" id="password" class="form-control">
    </div>
    <br>
<div class="form-group">
    <input type="submit" name="submit" class="btn btn-success col-md-12" value="Login">
</div>
<div v-if='messageFlag' style="margin-top:5%;">
                <div class="alert alert-danger center" style="width: 100%; margin-top: 5%;">
                    {{ message }}
            </div>
            </div>
      </form>
</div>
<div>
`,
methods: {
  login: function(){
      const self = this

      let login_info = document.getElementById('LoginForm')
      let LoginForm = new FormData(login_info)

      fetch("/api/auth/login",{
          method: "POST",
          body: LoginForm,
          headers: {
              'X-CSRFToken': token
          },
          credentials: 'same-origin'
      }).then(function(response){
          return response.json()
      }).then(function(jsonResponse){
          self.messageFlag = true

          if (jsonResponse.hasOwnProperty("token")){
              curr_user = {"token": jsonResponse.token, id: jsonResponse.user_id}
              localStorage.current_user = JSON.stringify(curr_user)

              router.go()
              router.push("/explore")
          }
          else{
              self.message = jsonResponse.errors
          }
      }).catch(function(error){
          self.messageFlag = false
          console.log(error)
      })
  }

},
data: function(){
  return {
      messageFlag: false,
      message: " "
  }
}

});

const Logout = Vue.component("logout", {
  template: `
  <div>
  <div/>`,
  created: function(){
    const self = this;
    
    fetch("api/auth/logout", {
      method: "GET"
    }).then(function(response){
      return response.json();
    }).then(function(jsonResponse){
      localStorage.removeItem("current_user");
      router.go();
      router.push("/");
    }).catch(function(error){
      console.log(error);
    });
  }
});


const NewPost = Vue.component('new-post', {
  template: `
  <div>
    <div v-if='messageFlag' >
      <div v-if="errorFlag">
        <div class="center" style="width: 100%; margin-top: 5%;">
          <ul class="alert alert-danger">
            <li v-for="error in message">
                {{ error }}
            </li>
          </ul>
        </div>
      </div>
      <div v-else class="alert alert-success center" style="width: 100%; margin-top: 5%;">
        {{ message }}
      </div>
    </div>
    
    <form class="center" id="npostform" @submit.prevent="submit">
      <div class="card-header center"><strong>New Post</strong></div>
      <div class="card center">
        <div class="card-body">
          	<label><strong>Photo</strong></label><br>
          	<input id="user_id" name="user_id" v-bind:value="cu_id" style="display: none;"/>
            <label class="btn" style="border: 0.5px solid black" for="photo"><strong>Browse</strong></label>
            <label>{{ filename }}</label>
            <br>
            <input type = "file" id="photo" name="photo" style="display: none;" v-on:change="updateFilename"/>
            <label style="margin-top: 5%"><strong>Caption</strong></label><br>
            <textarea id="caption" name="caption" style="width:100%" placeholder="Write a caption..."></textarea>
            <button id="submit" class = "btn btn-success">Submit</button>
        </div>    
      </div>
    </form>
  </div>
  `,
  methods: {
    updateFilename :function(){
        const self = this
        let filenameArr = $("#photo")[0].value.split("\\");
        self.filename = filenameArr[filenameArr.length-1]
    },
    submit: function(){
      self = this;
      
      fetch(`/api/users/${JSON.parse(localStorage.current_user).id}/posts`,{
        method: "POST",
        headers: {
          "Authorization": `Bearer ${JSON.parse(localStorage.current_user).token}`,
          'X-CSRFToken': token
        },
        body: new FormData(document.getElementById("npostform")),
        credentials: 'same-origin'
        
      }).then(function(response){
        return response.json();
      }).then(function(jsonResponse){
        self.messageFlag = true;
        
        if(jsonResponse.hasOwnProperty("message")){
          router.go()
          router.push(`/users/${self.cu_id}`)
        }else{
          self.errorFlag = true;
          self.message= jsonResponse.errors;
        }
      }).catch(function(error){
        console.log(error);
      });
    }
  },
  data: function(){
    return {
      filename: 'No File Selected',
      messageFlag: false,
      errorFlag: false,
      message: "",
      cu_id: JSON.parse(localStorage.current_user).id
    }
  }
  
});

const Register = Vue.component('registration',{
  template:`
  <div id ="register">
  <div class="container">
  <form id="registrationForm" @submit.prevent="registrationForm" method="POST" enctype="multipart/form-data">
  <div id="login-row" class="row justify-content-center align-items-center">
                <div id="login-column" class="col-md-6">
                    <div id="login-box" class="col-md-12">
    <h3 class="text-center text-info">Register</h3>
    <div class="form-group">
        <label for="username" class="text-info">Username</label><br>
        <input type="text" name="username" id="username" class="form-control">
      </div>
    <div class="form-group">
      <label for="password" class="text-info">Password</label><br>
      <input type="text" name="password" id="password" class="form-control">
    </div>
    <div class="form-group">
        <label for="firstname" class="text-info">Firstname</label><br>
        <input type="text" name="firstname" id="firstname" class="form-control">
      </div>
      <div class="form-group">
      <label for="lastname" class="text-info">Lastname</label><br>
      <input type="text" name="lastname" id="lastname" class="form-control">
    </div>
    <div class="form-group">
      <label for="email" class="text-info">Email</label><br>
      <input type="text" name="email" id="email" class="form-control">
    </div>
    <div class="form-group">
      <label for="location" class="text-info">Location</label><br>
      <input type="text" name="location" id="location" class="form-control">
    </div>
    <div class="form-group">
    <label for="biography" class="text-info">Biography</label><br>
    <textarea id="biography" class="form-control"></textarea>
  </div>
  <div class="form-group">
    <label for="photo">Photo</label>
    <input type="file" class="form-control-file" id="photo">
  </div>
<div class="form-group">
    <input type="submit" name="submit" class="btn btn-success col-md-12" value="Register">
</div>
</form>

</div>
<div>
`,
data: function(){
  return{
    errors:[],
    username:'',
    password:'',
    firstname:'',
    lastname:'',
    email:'',
    location:'',
    biography:'',
    photo:[]
  }
},
methods: {
  uploadform:function(e) {
    e.preventDefault();
    this.errors = [];
    if(!this.username){this.errors.push("Username required.");}
    if(!this.password){this.errors.push("Password required.");}
    if(!this.firstname){this.errors.push("Firstname required.");}
    if(!this.lastname){this.errors.push("Lastname required.");}
    if(!this.email){this.errors.push("Email required.");}
    if(!this.location){this.errors.push("Location required.");}
    if(!this.biography){this.errors.push("Biography required.");}
    if(!this.photo){this.errors.push("Photo required.");}
    
    let uploadForm = document.getElementById('registrationForm');
    let form_data = new FormData(uploadForm);
    fetch('/api/users/register', {
      method: 'POST',
      body: form_data,
      headers: {
          'X-CSRFToken': token
        },
        credentials: 'same-origin'
    })
      .then(function (response) {
        if (!response.ok) {
  throw Error(response.statusText);
}
   return response.json();
      })
      .then(function (jsonResponse) {
        if(jsonResponse.error) {
          this.errors.push(jsonResponse.error);
        }else{
          alert("Successfully Registered");

        console.log(jsonResponse);
        }
        
    })
      .catch(function (error) {
        console.log(error);
      });
    }
  }
});


const Explore = Vue.component("explore", {
  template:`
    <div class="row">
      <div v-if="postFlag" >
        <div class="alert alert-primary" >
          We Couldnt find any posts Anywhere. Be the first user to post on our site.
        </div>
      </div>
      <div v-else class="col-md-7" style="margin: 0 auto;">
        <div class="card" style=" width:100%; padding: 0; margin-bottom: 5%" v-for="(post, index) in posts">
          <ul class="list-group list-group-flush">
            <li class="list-group-item">
              <img id="pro-photo" v-bind:src=post.user_profile_photo style="width:40px"/>
              <router-link class="username" :to="{name: 'users', params: {user_id: post.user_id}}">{{ post.username }}</router-link>
            </li>
            <li class="list-group-item" style="padding: 0;">
              <img id="post-img" v-bind:src=post.photo style="width:100%" />
            </li>
            <li class="list-group-item text-muted">
              {{ post.caption }}
              <div class="row" style="margin-top: 10%">
                <div id="likes" class="col-md-6" style="text-align: left;">
                  <img class="like-ico liked" src="static/icons/liked.png"  v-on:click="like" style="width:20px; display: none;"/>
                  <img class="like-ico like" src="static/icons/like.png"  v-on:click="like" style="width:20px;"/> {{post.likes}} Likes
                  
                  <input type="hidden" id="post-id"  v-bind:value="post.id" />
                  <input type="hidden" id="post-index" v-bind:value="index" />
                </div>
                <div id="post-date" class="col-md-6" style="text-align: right">
                  {{post.created_on}}
                </div>
              </div>
            </li>
          </ul>
        </div>
      </div>
      
      <div class="col-md-3">
        	<router-link class="btn btn-primary" to="/posts/new" style="width:100%;">New Post</router-link>
      </div>
    </div>
  `,
  created: function(){
    self = this;
    
    fetch("/api/posts", {
      method: "GET",
      headers:{
        "Authorization": `Bearer ${JSON.parse(localStorage.current_user).token}`,
        'X-CSRFToken': token
      },
      credentials: 'same-origin'
    }).then(function(response){
      return response.json();
    }).then(function(jsonResponse){
      self.posts = jsonResponse.posts;
      self.postFlag = false;
    }).catch(function(error){
      console.log(error);
    });
  },
  methods: {
    like: function(event){
      self = this;
      let node_list = event.target.parentElement.children;
      let post_id = node_list[node_list.length-2].value;
      let post_index = node_list[node_list.length-1].value;
      
      fetch(`/api/posts/${post_id}/like`, {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${JSON.parse(localStorage.current_user).token}`,
          'X-CSRFToken': token,
          'Content-Type': 'application/json'
        },
        credentials: "same-origin",
        body: JSON.stringify({"user_id": JSON.parse(localStorage.current_user).id, "post_id": post_id})
      }).then(function(response){
        return response.json();
      }).then(function(jsonResponse){
        
        if(jsonResponse.hasOwnProperty("status")){
          if(jsonResponse.status == 201){
            event.target.style.display="none"
            event.target.previousElementSibling.style.display="";
            self.posts[post_index].likes = jsonResponse.likes;
          }
        }
      }).catch(function(error){
        console.log(error);
      });
    }
  },
  data: function(){
    return {
      posts: [],
      postFlag: true
    }
  }
});

const AllPost= Vue.component('allpost',{
  template: `
  <div>
  <div class="grid">
  <div></div>
  <div>
  </div>
  </div>
  </div>
  `
});

const Profile = Vue.component("profile",{
  template: `
  <div class="container">
	<div class="row">
                <div class="photo">
                  <img class="pic" src="{{url_for('static', filename='girl.jpg')}}"/>
                </div>
				<div class="aboutme">
        <h3 v-for="user in Users">{{user.username}}</h3>
        <br>
        <p v-for="user in Users">{{user.location}}</p><br>
        <p v-for="user in Users">{{user.joined_on}}</p>
        <p> v-for="user in Users">{{user.biography}}</p>
				</div>
         </div>
					 <div id="followers">
                    <div class= "col-sm">
                    <ul style ="list-style-type:none">
                        <li class= 'follow'>
                            <span id='f1'>6</span>
                            <span id='f3'>10</span>
                </li>

                <li class= "detail">
                    <span id= "d1">Posts</span>
                    <span id= "d3">Followers</span>
                </li>
             </ul>
            </div>
           </div>
                        
                <div class = "center">
				<button type="button" class="btn btn-default" >Follow</button>
                </div>
                <br>
			</div>
  `,
  methods: {
    follow: function(){
      self = this;
      
      fetch(`/api/users/${self.$route.params.user_id}/follow`,{
        method: "POST",
        headers: {
          "Authorization": `Bearer ${JSON.parse(localStorage.current_user).token}`,
          "Content-Type": "application/json",
          'X-CSRFToken': token
        },
        credentials: 'same-origin',
        body: JSON.stringify({"follower_id": JSON.parse(localStorage.current_user).id, "user_id": self.$route.params.user_id})
      }).then(function(response){
        return response.json();
      }).then(function(jsonResponse){
        
        if(jsonResponse.hasOwnProperty("message") && jsonResponse.status==201 ){
          $("#follow-btn")[0].innerHTML="Following";
          $("#follow-btn").removeClass("btn-primary");
          $("#follow-btn").addClass("btn-success")
          ++ self.user.followers;
        }
        
      }).catch(function(error){
        console.log(error)
      });
    }
  },
  created: function(){
    self = this;
    
    fetch(`/api/users/${self.$route.params.user_id}/posts`,{
      method: "GET",
      headers: {
        "Authorization": `Bearer ${JSON.parse(localStorage.current_user).token}`
      }
    }).then(function(response){
      return response.json();
    }).then(function(jsonResponse){
      self.user = jsonResponse.post_data;
    }).catch(function(error){
      console.log(error);
    });
  },
  data: function(){
    return {
      user: null,
      cu_id: (this.$route.params.user_id == JSON.parse(localStorage.current_user).id) ? true : false
    }
  }
});

// Define Routes
const router = new VueRouter({
    routes: [
        {path: "/", component: Home },
        {path: "/register", component: Register},
        {path: "/login", component: Login},
        {path: "/explore", component: Explore},
        {path: "/users/:user_id", name:"users",component: Profile},
        {path: "/posts/new", component: NewPost},
        {path: "/logout", component: Logout}
    ]
});

// Instantiate our main Vue Instance
let app = new Vue({
    el: "#app",
    router
});