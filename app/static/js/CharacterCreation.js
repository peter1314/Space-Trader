var difficultyNum;
var skillPoints;
var pilotSkills;
var fighterSkills;
var merchantSkills;
var engSkills;

/**
 * Sets the initial value of each skill to 0 and updates the HTML accordingly.
 */
function setDefaultVals() {
  pilotSkills = 0;
  fighterSkills = 0;
  merchantSkills = 0;
  engSkills = 0;

  updateSkills('pilot', 0);
  updateSkills('fighter', 0);
  updateSkills('merchant', 0);
  updateSkills('engineer', 0);
}

/**
 * Totals up the number of skill points applied. This is primarily checked against
 * skillPoints in order to discern whether the user has exceeded their allotted skill
 * limit.
 *
 * @return {number} The total number of points allocated to the user's skillset.
 */
function sumSkills() {
  return pilotSkills + fighterSkills + merchantSkills + engSkills;
}

/**
 * Updates the 'skillPoints' field to reflect the user-selected difficulty. Also edits
 * the styling of the <button> elements in CharacterCreation.html to indicate the current
 * difficulty.
 *
 * @param {number} ››› A value representing either easy, medium, or hard difficulty.
 */
function setSkillPoints(difficultyNumber) {
  difficultyNum = difficultyNumber;
  skillPoints = 20 - (4 * difficultyNum);

  if (difficultyNum === 1) {
    document.getElementById("easy").style = "background-color: #199619; filter: brightness(50%)"
    document.getElementById("medium").style = "background-color: #c8c819; filter: brightness(100%)"
    document.getElementById("hard").style = "background-color: #961919; filter: brightness(100%)"
  } else if (difficultyNum === 2) {
    document.getElementById("easy").style = "background-color: #199619; filter: brightness(100%)"
    document.getElementById("medium").style = "background-color: #c8c819; filter: brightness(50%)"
    document.getElementById("hard").style = "background-color: #961919; filter: brightness(100%)"
  } else if (difficultyNum === 3) {
    document.getElementById("easy").style = "background-color: #199619; filter: brightness(100%)"
    document.getElementById("medium").style = "background-color: #c8c819; filter: brightness(100%)"
    document.getElementById("hard").style = "background-color: #961919; filter: brightness(50%)"
  }

  setDefaultVals();
}

/**
 * Updates the player's default skills to reflect user input. In the character creation
 * page, incrementing or decrementing a particular skill calls this function, which then
 * checks the action's validity and updates accordingly.
 *
 * @param {string} type ››› The type of skill to be updated (e.g. pilot, fighter, etc).
 * @param {number} num ››› The amount by which the skill in incremented/decremented.
 */
function updateSkills(type, num) {
  if (sumSkills() + num <= skillPoints) {
    if (type == "pilot" && pilotSkills + num >= 0) {
      pilotSkills += num;
      document.getElementById("pSBNum").innerText = pilotSkills;
      document.getElementById("skillPoints").innerText = skillPoints - sumSkills();
    } else if (type == "fighter" && fighterSkills + num >= 0) {
      fighterSkills += num;
      document.getElementById("fSBNum").innerText = fighterSkills;
      document.getElementById("skillPoints").innerText = skillPoints - sumSkills();
    } else if (type == "merchant" && merchantSkills + num >= 0) {
      merchantSkills += num;
      document.getElementById("mSBNum").innerText = merchantSkills;
      document.getElementById("skillPoints").innerText = skillPoints - sumSkills();
    } else if (type == "engineer" && engSkills + num >= 0) {
      engSkills += num;
      document.getElementById("eSBNum").innerText = engSkills;
      document.getElementById("skillPoints").innerText = skillPoints - sumSkills();
    }
  }
}

/**
 * Assesses whether a trader can be created given the user's inputs (or lack thereof).
 * If the player's name is nonexistent or invalid, a pop-up box will require some form
 * of acceptable input in order to proceed. The same applies to when no difficulty has
 * been selected.
 *
 * @return {boolean} Whether or not a trader can be created.
 */
function canCreateTrader() {

  if (difficultyNum == null) {
    return false;
  }

  var nameBox = document.getElementById("playerNameBox").value.trim();
  if (nameBox.length == 0) {
    return false;
  }

  document.getElementById("nameInput").value = nameBox;
  document.getElementById("difficultyInput").value = difficultyNum;
  document.getElementById("pilotSkillsInput").value = pilotSkills;
  document.getElementById("fighterSkillsInput").value = fighterSkills;
  document.getElementById("merchantSkillsInput").value = merchantSkills;
  document.getElementById("engSkillsInput").value = engSkills;
  
  return true;
}
