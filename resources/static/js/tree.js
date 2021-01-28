'use strict';

const STORAGE_NAME = 'program_library';

let details = document.querySelectorAll('.treeHTML details');
let summary = document.querySelectorAll('.treeHTML details summary');
let category = document.querySelector('.category');

if(category != null){
    category.addEventListener('click', saveTree);
}

Array.from(summary).forEach(btn => {
  btn.addEventListener('click', saveTree);
});

document.addEventListener("DOMContentLoaded", pageReady);


function open_branches(current_branch){
    let branch;
    let parent_branch;
    if(current_branch != ''){
        for (let details_branch of details){
            if(details_branch.querySelector('summary a').innerHTML == current_branch){
                branch = details_branch;
                break;
            }
        }
        for (let i = 0; i < summary.length; i++){
            parent_branch = branch.parentNode.parentNode.parentNode.parentNode;
            let get_root = parent_branch.querySelector('.treeHTML');
            if(get_root == null) {
                let get_details = parent_branch.querySelector('details');
                get_details.setAttribute('open', 'open');
                branch=get_details;
            }
            else {
                break;
            }
        }
   }
}

function pageReady(event){
    let tree = [];
    let actual_branch;
    if (sessionStorage.getItem(STORAGE_NAME) == null || sessionStorage.getItem(STORAGE_NAME) == undefined){
        sessionStorage.setItem(STORAGE_NAME, tree = JSON.stringify({'tree_open_branches':[], 'actual_branch':[]}));
    }
    else {
        let category = document.getElementsByClassName('category')[0];
        if (category != null || category != undefined){
            actual_branch = category.textContent;
        }
        tree = JSON.parse(sessionStorage.getItem(STORAGE_NAME));
        if(tree['tree_open_branches'] != []){
            for (let branch of tree['tree_open_branches']){
                for (let details_branch of details) {
                    if(details_branch.querySelector('summary a').innerHTML == branch){
                        details_branch.setAttribute('open', 'open');
                    }
                }
            }
        }
        actual_branch = (actual_branch != undefined) ? actual_branch : tree['actual_branch'];
        if(tree['actual_branch'] != []){
            for (let details_branch of details){
                if(details_branch.querySelector('summary a').innerHTML == actual_branch){
                    details_branch.querySelector('summary a').classList.add('branchRed');
                    details_branch.setAttribute('open', 'open');
                }
            }
            open_branches(actual_branch);
        }
    }
}


function saveTree(event){
    let link = event.target;
    let session_branch = JSON.parse(sessionStorage.getItem(STORAGE_NAME))['actual_branch'];
    let tree_open_branches = [];
    for (let item of details) {
        if(item.hasAttribute('open')){
            tree_open_branches.push(item.querySelector('summary').textContent);
        }
    }
    let actual_branch = (event.target.tagName == 'A') ? event.target.textContent : session_branch;
    sessionStorage.setItem(STORAGE_NAME, JSON.stringify({'tree_open_branches': tree_open_branches, 'actual_branch': actual_branch}));
}
