import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { GlobalConstants } from 'src/app/global-constants';

@Component({
  selector: 'app-upload',
  templateUrl: './upload.component.html',
  styleUrls: ['./upload.component.css']
})
export class UploadComponent implements OnInit {

  selectedFile: File | null = null;

  url: String = "";

  addedUsers: string[] = [];

  userToRemove: string = "";

  maxView: number = 3;

  constructor(private http: HttpClient) { }

  ngOnInit(): void {
  }

  onFileSelected(event: any): void {


    document.getElementById("upload-icon")?.remove();
    let fileType = event.target!.files[0].name.split(".").pop().toUpperCase();
    let previewIcon: HTMLElement = document.getElementById("preview-icon")!;
    if (previewIcon.children[2]) previewIcon.children[2].remove();
    if (GlobalConstants.viewableFileTypes.includes(fileType)) {
      previewIcon.firstElementChild!.setAttribute("src", "assets/icons/file_types/" + fileType + ".svg");
    } else {
      let typeLabel = document.createElement("label");
      typeLabel.innerHTML = "." + fileType;
      typeLabel.style.fontSize = ((3 / fileType.length) > 1 ? 1 : 3 / fileType.length) + "rem";
      typeLabel.style.transform = "translateY(-70px)";
      previewIcon.append(typeLabel);
      previewIcon.firstElementChild!.setAttribute("src", "assets/icons/file_types/unknown.svg");
    }
    var displayName = event.target!.files[0].name
    if (event.target!.files[0].name.length > 16) displayName = displayName.substring(0, 16).trim() + "...";
    previewIcon.children[1].innerHTML = displayName;
    previewIcon.style.height = "100px";
    previewIcon.classList.toggle("fileAppear");
    previewIcon.classList.toggle("fileAppear2");

    // this.selectedFile = event.target.files[0];
    // const fd = new FormData();
    // fd.append('image', this.selectedFile!, this.selectedFile!.name);
    // this.http.post('omegashare.test', fd).subscribe(res => {
    //   console.log(res);
    // })


    // if(event.target.files) {
    //   let reader = new FileReader();
    //   reader.readAsDataURL(event.target.files[0]);
    //   reader.onload = (event:any) => {
    //     this.url = event.target.result;
    //   }
    // }

  }

  addUser(event: KeyboardEvent): void {
    document.getElementById("add-user-error")!.style.display = "none";
    let regexEmail: RegExp = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    let regexUsername: RegExp = /^[a-zA-Z0-9\_]+$/;
    let value: string = (<HTMLInputElement>document.getElementById("user-selector")).value;
    if (event.key == "Enter" && value.length > 0) {
      if (this.addedUsers.includes(value)) {
        this.giveInputError("already added this user");
        return;
      }
      if (value.match(regexEmail)) {
        this.addToUsers(value);
      } else if (value.includes('@')) {
        this.giveInputError("invalid email");
        return;
      } else if (value.match(regexUsername)) {
        this.addToUsers(value);
      } else {
        this.giveInputError('"' + value.replace(/[a-zA-Z0-9-_]/g, '')[0] + '"' + " cannot be in a username");
        return;
      }

    }
  }

  giveInputError(str: string): void {
    document.getElementById("add-user-error")!.innerHTML = str;
    document.getElementById("add-user-error")!.style.display = "block";
  }

  addToUsers(user: string): void {
    this.addedUsers.unshift(user);
    let newElement: HTMLElement = <HTMLElement>document.getElementById("added-user-template")?.firstElementChild?.cloneNode(true);
    newElement.innerHTML = user + newElement.innerHTML;
    newElement.id = user;
    newElement.getElementsByTagName("svg")[0].addEventListener("click", e => {
      this.removeUser(e);
    })
    let addedUsersEl: HTMLElement = <HTMLElement>document.getElementById("added-users");
    addedUsersEl.prepend(newElement);
    newElement.classList.add("appearing");
    setTimeout(() => {
      newElement.classList.remove("appearing");      
    }, 0);
    if(this.addedUsers.length > this.maxView) {
      document.getElementById(this.addedUsers[this.maxView])?.classList.add("hide");
      document.getElementById("show-more-less")!.innerHTML = "show all";
      document.getElementById("show-more-less")?.classList.add("shown");
      document.getElementById("and-more")?.classList.add("shown");
      document.getElementById("added-users")!.style.minHeight = "5.4rem";
    }
    (<HTMLInputElement>document.getElementById("user-selector")).value = "";
  }

  removeUser(event: Event) {
    // AFMAKEN
    event.composedPath().forEach(e => { if ((<HTMLElement>e).classList && (<HTMLElement>e).classList.contains("addedUser")) this.userToRemove = (<HTMLElement>e).id })
    this.addedUsers.splice(this.addedUsers.indexOf(this.userToRemove), 1);
    document.getElementById(this.userToRemove)!.classList.add("vanishing");
    setTimeout(() => {
      document.getElementById(this.userToRemove)!.outerHTML = "";
      this.userToRemove = "";
    }, 200);
    if(this.addedUsers.length > this.maxView) document.getElementById(this.addedUsers[this.maxView - 1])?.classList.remove("hide");
    if(this.addedUsers.length <= this.maxView) {
      if (document.getElementById("show-more-less")!.classList.contains("shown")) {
        Array.from(document.getElementsByClassName("addedUser")).forEach(e => {
          if(e.classList.contains("hide")) e.classList.remove("hide");
        });
        document.getElementById("show-more-less")!.classList.remove("shown");
        document.getElementById("and-more")!.classList.remove("shown");
        document.getElementById("added-users")!.style.minHeight = "";
      }
    }    
  }
  
  toggleShowMore() {
    if(this.addedUsers.length > this.maxView) {      
      if (document.getElementById("show-more-less")?.classList.contains("less")) {      
        Array.from(document.getElementsByClassName("addedUser")).forEach(e => {
          if(e.classList.contains("hide")) e.classList.remove("hide");
          document.getElementById("and-more")!.classList.remove("shown");
        });
        document.getElementById("show-more-less")!.innerHTML = "show less";
      } else {
        for (let i = this.maxView; i < this.addedUsers.length; i++) {
          document.getElementById(this.addedUsers[i])?.classList.add("hide");
          document.getElementById("show-more-less")!.innerHTML = "show all";
          document.getElementById("and-more")!.classList.add("shown");
        }
      }
      document.getElementById("show-more-less")?.classList.toggle("less");
    }
  }
}
