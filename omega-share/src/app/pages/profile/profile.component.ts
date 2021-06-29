import { Component, OnInit } from '@angular/core';
import { TokenStorageService } from '../../_services/token-storage.service';
import { UserService } from '../../_services/user.service';
import { User } from '../../user'
import { Router } from '@angular/router';
import { AuthService } from 'src/app/_services/auth.service';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit {

  profilePicture: string = "assets/placeholder pictures/stock_profile_picture.png";
  amountOfPosts: number = 12;
  likes: number = 0;
  banner: string = "assets/placeholder pictures/stock banner.jpg";
  fileTypes: string[] = ["ACC", "AE", "AI", "AN", "AVI", "BMP", "CSV", "DAT", "DGN", "DOC", "DOCH", "DOCM", "DOCX", "DOTH", "DW", "DWFX"];
  
  isSuccessful: any;
  user: any;

  errorMessage: any;
  constructor(private userService: UserService, private token: TokenStorageService, private authService: AuthService, private router: Router) { }

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

}
