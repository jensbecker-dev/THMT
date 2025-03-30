document.addEventListener("DOMContentLoaded", () => {
    const stats = {
        rank: "281542",
        roomsCompleted: 120,
        challengesSolved: 22,
        badgesEarned: 6,
        points: 4500,
    };

    document.getElementById("stat-rank").textContent = stats.rank;
    document.getElementById("stat-rooms").textContent = stats.roomsCompleted;
    document.getElementById("stat-challenges").textContent = stats.challengesSolved;
    document.getElementById("stat-badges").textContent = stats.badgesEarned;
    document.getElementById("stat-points").textContent = stats.points;
});