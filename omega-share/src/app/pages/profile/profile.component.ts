import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit {

  profilePicture: string = "assets/placeholder pictures/stock_profile_picture.png";

  firstName: string = "John";

  lastName: string = "Doe";

  username: string = "JognDoe99";

  amountOfPosts: number = 0;

  likes: number = 0;

  about: string = "Empty";

  banner: string = "assets/placeholder pictures/stock banner.jpg";

  fileTypes: string[] = ["ACC", "AE", "AI", "AN", "AVI", "BMP", "CSV", "DAT", "DGN", "DOC", "DOCH", "DOCM", "DOCX", "DOTH", "DW", "DWFX"];

  constructor() { }

  ngOnInit(): void {
    document.getElementById("banner")!.style.backgroundImage = "url('" + this.banner + "')";
  }

  getRandomType(): string {
    return this.fileTypes[Math.floor(Math.random() * 16)];
  }

}
