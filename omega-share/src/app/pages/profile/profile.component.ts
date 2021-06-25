import { Component, OnInit } from '@angular/core';
import { TokenStorageService } from '../../_services/token-storage.service';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit {

  profilePicture: string = "assets/placeholder pictures/stock_profile_picture.png";
  firstName: string = "John";
  lastName: string = "Doe";
  username: string = "JohnDoe99";
  email: string = "JohnDoe@sample.com";
  amountOfPosts: number = 12;
  likes: number = 0;
  about: string = "Empty";
  banner: string = "assets/placeholder pictures/stock banner.jpg";
  fileTypes: string[] = ["ACC", "AE", "AI", "AN", "AVI", "BMP", "CSV", "DAT", "DGN", "DOC", "DOCH", "DOCM", "DOCX", "DOTH", "DW", "DWFX"];

  constructor(private token: TokenStorageService) { }

  ngOnInit(): void {
    document.getElementById("banner")!.style.backgroundImage = "url('" + this.banner + "')";
    const user = this.token.getUser();
    this.email = user.email;
    this.username = user.username;

  }

  getRandomType(): string {
    return this.fileTypes[Math.floor(Math.random() * 16)];
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

}
