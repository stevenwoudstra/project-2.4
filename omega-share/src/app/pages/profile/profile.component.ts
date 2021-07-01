import { Component, OnInit } from '@angular/core';
import { TokenStorageService } from '../../_services/token-storage.service';
import { UserService } from '../../_services/user.service';
import { User } from '../../user'
import { Router } from '@angular/router';
import { AuthService } from 'src/app/_services/auth.service';
import { FileService } from 'src/app/_services/file.service';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit {

  profilePicture: any;
  profilePictureBack: string = "assets/placeholder pictures/stock_profile_picture.png";
  isImageLoading: boolean = true;

  amountOfPosts: number = 12;
  likes: number = 0;
  banner: string = "assets/placeholder pictures/stock banner.jpg";
  fileTypes: string[] = ["ACC", "AE", "AI", "AN", "AVI", "BMP", "CSV", "DAT", "DGN", "DOC", "DOCH", "DOCM", "DOCX", "DOTH", "DW", "DWFX"];
  
  isSuccessful: any;
  user: any;

  errorMessage: any;
  constructor(private userService: UserService, private token: TokenStorageService, private authService: AuthService, private router: Router, private fileService: FileService) { }

  ngOnInit(): void {
    const userToken = this.token.getUser();
    this.user = new User(
      userToken.userid,
      userToken.username,
      userToken.role,
      );
      console.log(this.user);
    document.getElementById("banner")!.style.backgroundImage = "url('" + this.banner + "')";

    this.userService.getUserProfile().subscribe(
      data => {
        this.user.email = data.email;
        this.user.firstName = data.first_name;
        this.user.lastName = data.last_name;
        this.user.about = data.bio;
        console.log(data.profile_picture);
        if(data.profile_picture =! null) {
          this.getImageFromService();
          console.log("kaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaas");
        } else{ 
          this.isImageLoading = false
        }
      },
      err => {
        this.errorMessage = err.error.message;
      }
    );
    console.log(this.user);
  }

  getRandomType(): string {
    return this.fileTypes[1];
  }

  editBtn(): void {
    document.getElementById("edit-field")?.classList.toggle("enabled");
    if(document.getElementById("edit-field")?.classList.contains("enabled")) {
      document.getElementById("edit-profile-btn")!.innerHTML = "cancel";
      document.getElementById("dropzone")!.classList.remove("disabled");
      document.getElementById("dropzone")!.classList.add("enabled");
    } else {
      document.getElementById("edit-profile-btn")!.innerHTML = "edit profile";
      document.getElementById("dropzone")!.classList.add("disabled");
      document.getElementById("dropzone")!.classList.remove("enabled");
    }
  }

  onSubmit(): void {
    console.log(this.user)
    this.userService.updateUserProfile(this.user.email, this.user.firstName, this.user.lastName).subscribe(
      data => {
        console.log(data);
        this.isSuccessful = true;
        this.editBtn();
      },
      err => {
        this.errorMessage = err.error.message;
        this.isSuccessful = false;
      }
    );
  }

  onFileSelected(event: any): void {
    console.log(event)
    const file = event.target.files[0];
    if (file != null){
      this.fileService.postProfilePicture(file).subscribe(
        data => {
          this.getImageFromService()
        },
        err => {
        }
      );
    }
  }

  createImageFromBlob(image: Blob) {
    let reader = new FileReader();
    reader.addEventListener("load", () => {
       this.profilePicture = reader.result;
    }, false);
 
    if (image) {
       reader.readAsDataURL(image);
    }
   }

   getImageFromService() {
    this.isImageLoading = true;
    this.userService.getProfilePicture().subscribe(data => {
      this.createImageFromBlob(data);
      this.isImageLoading = false;
    }, error => {
      this.isImageLoading = false;
      console.log(error);
    });
}
}
