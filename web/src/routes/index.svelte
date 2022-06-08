<script lang="ts">
	interface Insight {
		departmentName: string
		employeeEmail: string
		employeeName: string
		id: string
		managerEmail: string
		managersName: string
	}

	let insightQuery = `
      query MyQuery {
        getInsight(skip: 0, limit: 5) {
          departmentName
          employeeEmail
          employeeName
          id
          managerEmail
          managersName
        }
      }
`
	const defaultFields = [
		'id',
		'departmentName',
		'employeeEmail',
		'employeeName',
		'managerEmail',
		'managersName'
	]

	const buildQuery = (skip: number = 0, limit: number = 5, fields: string[] = defaultFields) => {
		return `
      query MyQuery {
        getInsight(skip: ${skip}, limit: ${limit}) {
          ${fields.join(' ')}
        }
      }
    `
	}

	// The callback way
	// const fetchInsight: Promise<Insight[]> = fetch('http://localhost:2000/graphql', {
	// 	method: 'POST',
	// 	headers: {
	// 		'Content-Type': 'application/json'
	// 	},
	// 	body: JSON.stringify({
	// 		query: insightQuery
	// 	})
	// })
	// 	.then((res) => res.json())
	// 	.then((result) => {
	// 		console.log('lol')
	// 		return result.data.getInsight
	// 	})

	// The "oldschool" way
	const fetchInsight = async (): Promise<Insight[]> => {
		const res = await fetch('http://localhost:2000/graphql', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				query: insightQuery
			})
		})

		const result = await res.json()
		return result.data.getInsight
	}

	let data = fetchInsight()

	const refresh = () => {
		data = fetchInsight()
	}

	const modifyData = (event: Event) => {
		const data = new FormData(event.target)

		let selectedFields: string[] = []
		for (const x of data.entries()) {
			if (x[1] === 'on') {
				selectedFields.push(x[0])
			}
		}

		insightQuery = buildQuery(data.get('skip'), data.get('limit'), selectedFields)
		refresh()
	}
</script>

<h1>Velkommen til indsigt</h1>

<form class="content" on:submit|preventDefault={modifyData}>
	<label for="skip">Skip</label>
	<input name="skip" type="number" value="0" />
	<label for="limit">Limit</label>
	<input name="limit" type="number" value="5" />
	<label for="fields">Fields</label>
	{#each defaultFields as field}
		<input name={field} type="checkbox" checked />
		{field}
		<br />
	{/each}
	<button type="submit">Submit</button>
</form>

<br />
{#await data}
	Henter...
{:then insights}
	{#each insights as insight}
		{#each Object.values(insight) as field}
			{field}
			<br />
		{/each}
		<br />
	{/each}
{/await}
